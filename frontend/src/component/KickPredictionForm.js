import { useState } from "react";
import axios from "axios";
import "./KickPredictionForm.css"; // Import the CSS file

export default function KickPredictionForm() {
  const [features, setFeatures] = useState({
    speed: "",
    angle: "",
    distance: "",
    goalkeeper_position: "",
  });
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setFeatures({ ...features, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post("http://127.0.0.1:5000/predict", {
        features: Object.values(features).map(Number),
      });
  
      // Convert the prediction into a meaningful message
      const binaryPrediction = response.data.prediction >= 0.5 ? 1 : 0;
      const predictionMessage = binaryPrediction === 1 ? "Goal! 🎯" : "Missed ❌";
  
      setPrediction(predictionMessage);
    } catch (err) {
      setError("Error fetching prediction. Check if the backend is running.");
    }
    setLoading(false);
  };

  const handleReset = () => {
    setFeatures({ speed: "", angle: "", distance: "", goalkeeper_position: "" });
    setPrediction(null);
    setError(null);
  };

  return (
    <div className="kick-form-container">
      <div className="kick-form-box">
        <h1 className="kick-form-title">⚽ Kick Success Predictor</h1>

        <form onSubmit={handleSubmit}>
          {[
            { key: "speed", label: "Speed", placeholder: "Enter speed (m/s)" },
            { key: "angle", label: "Angle", placeholder: "Enter angle (degrees)" },
            { key: "distance", label: "Distance", placeholder: "Enter distance (m)" },
            { key: "goalkeeper_position", label: "Goalkeeper Position", placeholder: "Enter goalkeeper position" },
          ].map(({ key, label, placeholder }, index) => (
            <div key={index} className="kick-form-group">
              <label htmlFor={key} className="kick-form-label">
                {label}
              </label>
              <input
                id={key}
                type="number"
                name={key}
                value={features[key]}
                onChange={handleChange}
                className="kick-form-input"
                placeholder={placeholder}
                required
              />
            </div>
          ))}

          <div className="kick-form-buttons">
            <button type="submit" className="kick-form-predict-btn" disabled={loading}>
              {loading ? "Predicting..." : "Predict"}
            </button>
            <button type="button" onClick={handleReset} className="kick-form-reset-btn">
              Reset
            </button>
          </div>
        </form>

        {error && <p className="text-red-500 mt-4 text-center">{error}</p>}

        {prediction !== null && (
          <div className="kick-form-result">
            Prediction: {typeof prediction === "number" ? prediction.toFixed(4) : prediction}
          </div>
        )}
      </div>
    </div>
  );
}
