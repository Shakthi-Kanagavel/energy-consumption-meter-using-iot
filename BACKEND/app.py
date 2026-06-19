from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
from ml_model import predict_next_power  # import ML function

app = Flask(__name__)
CORS(app)

# -----------------------------
# MongoDB connection
# -----------------------------
client = MongoClient("mongodb://localhost:27017/")
db = client["energy_db"]
collection = db["energy_data"]

POWER_THRESHOLD = 200  # W
MAINS_V = 230.0
POWER_FACTOR = 0.95


# -----------------------------
# ROUTES
# -----------------------------

# ESP32 → sends data here
@app.route('/api/sensor', methods=['POST'])
def add_data():
    try:
        data = request.get_json(force=True)

        current = float(data.get("current", 0))
        power = float(data.get("power", 0))

        record = {
            "current": current,
            "power": round(power, 2),
            "timestamp": datetime.now()
        }

        collection.insert_one(record)

        return jsonify({"status": "success", "message": "Data saved"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


# Frontend → fetches data here
@app.route('/api/get', methods=['GET'])
def get_data():
    try:
        data = list(collection.find().sort("timestamp", -1).limit(10))

        if not data:
            return jsonify({"readings": [], "predicted_power": None, "alert": None})

        for item in data:
            item["_id"] = str(item["_id"])
            item["timestamp"] = item["timestamp"].strftime("%Y-%m-%d %H:%M:%S")

        # Prediction
        powers = [d["power"] for d in reversed(data)]
        predicted_next = predict_next_power(powers)

        # Alert
        latest_power = data[0]["power"]
        alert_status = None
        if latest_power > POWER_THRESHOLD:
            alert_status = f"⚠ High Power Usage: {latest_power} W exceeds {POWER_THRESHOLD} W limit!"

        return jsonify({
            "readings": data,
            "predicted_power": predicted_next,
            "alert": alert_status
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
