from flask import Flask, request, jsonify
from flask_cors import CORS
from fake_news_detector import FakeNewsDetector

app = Flask(__name__)

# ✅ Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize fake news detector
detector = FakeNewsDetector()

# Load trained model
model_loaded = detector.load_model("fake_news_model.pkl")
if not model_loaded:
    print("❌ Failed to load model. Please retrain the model.")

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Fake Media Detection API is running"
    })

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Safely read JSON data
        data = request.get_json(force=True)
        print("📩 Received data:", data)

        # Check if model is ready
        if not detector.is_trained:
            return jsonify({
                "error": "Model not trained or not loaded"
            }), 500

        # Validate input text
        if "text" not in data or not data["text"].strip():
            return jsonify({
                "error": "Text is required"
            }), 400

        # Make prediction
        result = detector.predict(data["text"])
        print("✅ Prediction:", result)

        return jsonify(result)

    except Exception as e:
        # Print exact backend error
        print("🔥 Backend Error:", e)
        return jsonify({
            "error": str(e)
        }), 500

if __name__ == "__main__":
    # ❌ Disable reloader to avoid double execution
    app.run(debug=True, use_reloader=False)
