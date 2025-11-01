from flask import Flask, render_template, request, jsonify
import pandas as pd
from flask_cors import CORS
import os

app = Flask(__name__, static_folder="../frontend", template_folder="../frontend")
CORS(app)

# Data paths
data_dir = os.path.join(os.path.dirname(__file__), "data")
rainfall_path = os.path.join(data_dir, "rainfall_state_year.csv")
agri_path = os.path.join(data_dir, "agri_production_state_year.csv")

# Load datasets
rainfall_df = pd.read_csv(rainfall_path)
agri_df = pd.read_csv(agri_path)

@app.route("/")
def home():
    return app.send_static_file("index.html")

@app.route("/compare", methods=["POST"])
def compare():
    data = request.get_json()
    state1 = data.get("state1")
    state2 = data.get("state2")

    if not state1 or not state2:
        return jsonify({"error": "Please select both states."}), 400

    # Get data for selected states
    rain1 = rainfall_df[rainfall_df["State"] == state1]
    rain2 = rainfall_df[rainfall_df["State"] == state2]

    agri1 = agri_df[agri_df["State"] == state1]
    agri2 = agri_df[agri_df["State"] == state2]

    # Calculate averages
    result = {
        "state1": {
            "name": state1,
            "avg_rainfall": round(rain1["Rainfall"].mean(), 2) if not rain1.empty else "N/A",
            "avg_production": round(agri1["Production"].mean(), 2) if not agri1.empty else "N/A"
        },
        "state2": {
            "name": state2,
            "avg_rainfall": round(rain2["Rainfall"].mean(), 2) if not rain2.empty else "N/A",
            "avg_production": round(agri2["Production"].mean(), 2) if not agri2.empty else "N/A"
        }
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
