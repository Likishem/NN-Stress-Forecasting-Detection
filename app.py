from flask import Flask, jsonify, request
import numpy as np
from stress_model import model, scaler  # import your trained model and scaler

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Stress Level Classifier API!"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    features = np.array([[data['heart_rate'], data['skin_conductance'], data['body_temp'], data['respiration_rate']]])
    features_scaled = scaler.transform(features)
    pred = model.predict(features_scaled)
    return jsonify({'predicted_stress_level': int(pred[0])})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
