from flask import Flask, request, jsonify  # Import Flask for creating the API, request for handling incoming data, and jsonify for JSON responses.
import pickle  # Import pickle to load the pre-trained machine learning models and vectorizer.

# Initialize the Flask application.
app = Flask(__name__)

# ---------------------------------------------------------
# Model Loading Section
# ---------------------------------------------------------
# Load the preprocessed data artifacts (specifically the vectorizer) at server startup.
# This ensures we don't reload the file for every request, optimizing performance.
with open("data/preprocessed_data.pkl", "rb") as f:
    # We only need the vectorizer here to transform incoming email text.
    # The first two elements (X, y) are training data and are ignored using `_`.
    _, _, vectorizer = pickle.load(f)

# Load the trained Random Forest Classifier model.
with open("models/phishing_rf.pkl", "rb") as f:
    rf_model = pickle.load(f)

# Load the trained Stochastic Gradient Descent (SGD) Classifier model.
with open("models/phishing_sgd.pkl", "rb") as f:
    sgd_model = pickle.load(f)

# ---------------------------------------------------------
# API Routes
# ---------------------------------------------------------
@app.route("/predict", methods=["POST"])
def predict():
    """
    API Endpoint to predict if an email is phishing or not.
    Expects a JSON payload with an "email_text" key.
    
    Returns:
        JSON response containing predictions from both Random Forest and SGD models.
    """
    # Parse the JSON data from the incoming POST request.
    data = request.json
    
    # Extract the email text from the request data. Default to empty string if missing.
    email_text = data.get("email_text", "")

    # Transform the raw email text into a numerical feature vector using the loaded TF-IDF vectorizer.
    # The vectorizer expects a list of strings, hence [email_text].
    # .toarray() converts the sparse matrix to a dense array for the models.
    email_vector = vectorizer.transform([email_text]).toarray()
    
    # Generate prediction using the Random Forest model.
    # Returns [0] or [1], so we access the first element.
    rf_pred = rf_model.predict(email_vector)[0]
    
    # Generate prediction using the SGD model.
    sgd_pred = sgd_model.predict(email_vector)[0]

    # Construct the response dictionary mapping numerical predictions to human-readable labels.
    # 1 indicates "Phishing", 0 indicates "Not Phishing".
    response = {
        "RandomForest": "Phishing" if rf_pred == 1 else "Not Phishing",
        "SGDClassifier": "Phishing" if sgd_pred == 1 else "Not Phishing"
    }
    
    # Return the response as a JSON object with a 200 OK status.
    return jsonify(response)

# ---------------------------------------------------------
# Server Entry Point
# ---------------------------------------------------------
if __name__ == "__main__":
    # Start the Flask development server.
    # host="0.0.0.0" makes the server accessible externally (e.g., from other devices on the network).
    # port=5000 is the standard port for Flask applications.
    app.run(host="0.0.0.0", port=5000)
