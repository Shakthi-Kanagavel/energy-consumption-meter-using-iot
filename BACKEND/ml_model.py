import numpy as np
from sklearn.linear_model import LinearRegression

def predict_next_power(power_values):
    """
    Predict next power value using Linear Regression.
    :param power_values: list of recent power readings [p1, p2, p3...]
    :return: float or None
    """
    if len(power_values) < 2:
        return None

    X = np.arange(len(power_values)).reshape(-1, 1)
    y = np.array(power_values)

    model = LinearRegression()
    model.fit(X, y)

    next_val = model.predict([[len(power_values)]])
    return round(float(next_val), 2)
