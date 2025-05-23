from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import joblib
import numpy as np

app = Flask(__name__)  # Use name here
CORS(app)  # Enable CORS for all routes

@app.route('/')
def home():
    return "Welcome to my Flask app!"

# Load the model
model = joblib.load('afib_model.pkl')  # Ensure this file is in the same directory

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        # Extract features
        heart_rate = data['HeartRate']
        spo2 = data['SpO2']
        temperature = data['Temperature']
        
        # Prepare the feature array
        features = np.array([[heart_rate, spo2, temperature]])
        
        # Make prediction
        prediction = model.predict(features)
        
        return jsonify({'prediction': int(prediction[0])})  # Convert prediction to int
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)