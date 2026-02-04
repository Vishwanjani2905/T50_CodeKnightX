from flask import Flask, render_template, jsonify
import pandas as pd
import numpy as np
import base64
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend to avoid threading issues
import matplotlib.pyplot as plt
from io import BytesIO
import threading
import time

app = Flask(__name__)

# Simulated warehouse temperature zones
def generate_temp_zones():
    return pd.DataFrame({
        "zone_id": ["ZONE_1", "ZONE_2", "ZONE_3"],
        "rack_id": ["R1", "R2", "R3"],
        "efficiency_score": np.random.rand(3) * 100
    })

def generate_heatmap(temp_zones):
    pivot_table = temp_zones.pivot(index="zone_id", columns="rack_id", values="efficiency_score")
    plt.figure(figsize=(6,4))
    plt.imshow(pivot_table, cmap='coolwarm', aspect='auto')
    plt.colorbar(label="Efficiency Score")
    plt.xticks(ticks=range(len(pivot_table.columns)), labels=pivot_table.columns)
    plt.yticks(ticks=range(len(pivot_table.index)), labels=pivot_table.index)
    plt.xlabel("Rack ID")
    plt.ylabel("Zone ID")
    plt.title("Temperature Efficiency Heatmap")
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()  # Close figure to avoid memory leaks
    return base64.b64encode(buf.read()).decode('utf-8')

def update_data():
    global temp_zones, heatmap_url
    while True:
        temp_zones = generate_temp_zones()
        heatmap_url = generate_heatmap(temp_zones)  # Update heatmap on new data
        time.sleep(60)  # Delay before updating data

temp_zones = generate_temp_zones()
heatmap_url = generate_heatmap(temp_zones)  # Initialize with first heatmap
threading.Thread(target=update_data, daemon=True).start()

@app.route('/')
def index():
    return render_template("index.html", temp_zones=temp_zones.to_dict(orient='records'), heatmap_url=heatmap_url)

@app.route('/data')
def data():
    return jsonify({
        "temp_zones": temp_zones.to_dict(orient='records'),
        "heatmap_url": heatmap_url
    })

if __name__ == '__main__':
    app.run(port=5002,debug=True)