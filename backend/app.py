from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import pickle
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the trained model and scaler
model = tf.keras.models.load_model("football_model.h5")
scaler = pickle.load(open("scaler.pkl", "rb"))

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get JSON input from request
        data = request.get_json()

        # Validate the input
        if not data or "features" not in data:
            return jsonify({"error": "Missing 'features' key"}), 400

        # Convert to NumPy array and reshape
        features = np.array(data["features"]).reshape(1, -1)

        # Scale the input
        scaled_features = scaler.transform(features)

        # Make prediction
        prediction = model.predict(scaled_features)

        # Return prediction as JSON
        return jsonify({"prediction": prediction.tolist()})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
