let chart;

async function fetchData() {
    try {
        
        const res = await fetch("http://127.0.0.1:5000/api/get");
        const response = await res.json();
        const data = response.readings;
        const predictedPower = response.predicted_power;

        if (data.length > 0) {
            // Update values
            document.getElementById("current").innerText = data[0].current + " A";
            document.getElementById("power").innerText = data[0].power + " W";
            document.getElementById("timestamp").innerText = "Last Updated: " + data[0].timestamp;
            document.getElementById("prediction").innerText =
                "Predicted Next Power: " + (predictedPower !== null ? predictedPower + " W" : "--");

            // Prepare chart data
            const labels = data.map(d => d.timestamp).reverse();
            const powerData = data.map(d => d.power).reverse();

            if (!chart) {
                const ctx = document.getElementById('myChart').getContext('2d');
                chart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Power (W)',
                            data: powerData,
                            borderColor: '#0d6efd',
                            backgroundColor: 'rgba(13,110,253,0.1)',
                            fill: true,
                            tension: 0.3,
                            pointRadius: 3
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: { display: true }
                        },
                        scales: {
                            x: { 
                                ticks: { maxRotation: 90, minRotation: 45 },
                                grid: { display: false }
                            },
                            y: {
                                beginAtZero: true,
                                grid: { color: '#e9ecef' }
                            }
                        }
                    }
                });
            } else {
                chart.data.labels = labels;
                chart.data.datasets[0].data = powerData;
                chart.update();
            }
        }
    } catch (err) {
        console.error("Error fetching data:", err);
    }
}

// Auto-refresh every 60s
setInterval(fetchData, 60000);
fetchData();
