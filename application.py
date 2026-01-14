from flask import Flask, jsonify, request, render_template
import logging
import joblib
import numpy as np
import os

app = Flask(__name__)

MODEL_PATH = 'artifacts/model/logistic_regression_model.pkl'
SCALER_PATH = 'artifacts/processed/scaler.pkl'

# Load model and scaler
try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    print("[SUCCESS] Model and scaler loaded successfully")
except Exception as e:
    print(f"[ERROR] Error loading model/scaler: {e}")
    model, scaler = None, None

FEATURES = ['Operation_Mode', 'Temperature_C', 'Vibration_Hz',
                'Power_Consumption_kW', 'Network_Latency_ms', 'Packet_Loss_%',
                'Quality_Control_Defect_Rate_%', 'Production_Speed_units_per_hr',
                'Predictive_Maintenance_Score', 'Error_Rate_%', 'Year', 'Month', 'Day', 'Hour'
            ]

LABELS = {
    0: 'Low Efficiency',
    1: 'Medium Efficiency', 
    2: 'High Efficiency'
}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template('index.html', features=FEATURES)
    
    prediction = None
    confidence = None
    
    if request.method == "POST":
        try:
            if model is None or scaler is None:
                return jsonify({"error": "Model not loaded"}), 500
                
            data = request.get_json()
            input_data = [data[feature] for feature in FEATURES]
            input_array = np.array(input_data).reshape(1, -1)
            input_scaled = scaler.transform(input_array)
            
            pred_class = model.predict(input_scaled)[0]
            pred_proba = model.predict_proba(input_scaled)[0]
            confidence = float(max(pred_proba))
            
            prediction = LABELS.get(pred_class, "Unknown")
            
            return jsonify({
                "prediction": prediction,
                "confidence": confidence,
                "class": int(pred_class)
            })
            
        except Exception as e:
            logging.error(f"Error during prediction: {e}")
            return jsonify({"error": "Invalid input data"}), 400

@app.route("/predict", methods=["POST"])
def predict():
    try:
        if model is None or scaler is None:
            return jsonify({"error": "Model not loaded"}), 500
            
        data = request.get_json()
        input_data = [data[feature] for feature in FEATURES]
        input_array = np.array(input_data).reshape(1, -1)
        input_scaled = scaler.transform(input_array)
        
        pred_class = model.predict(input_scaled)[0]
        pred_proba = model.predict_proba(input_scaled)[0]
        confidence = float(max(pred_proba))
        
        prediction = LABELS.get(pred_class, "Unknown")
        
        return jsonify({
            "prediction": prediction,
            "confidence": confidence,
            "class": int(pred_class),
            "probabilities": {
                "Low Efficiency": float(pred_proba[0]),
                "Medium Efficiency": float(pred_proba[1]), 
                "High Efficiency": float(pred_proba[2])
            }
        })
        
    except Exception as e:
        logging.error(f"Error during prediction: {e}")
        return jsonify({"error": str(e)}), 400

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "scaler_loaded": scaler is not None
    })

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
