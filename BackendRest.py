from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

# Load vectorizer and models once at server start
with open("data/preprocessed_data.pkl", "rb") as f:
    _, _, vectorizer = pickle.load(f)

with open("models/phishing_rf.pkl", "rb") as f:
    rf_model = pickle.load(f)

with open("models/phishing_sgd.pkl", "rb") as f:
    sgd_model = pickle.load(f)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    email_text = data.get("email_text", "")

    email_vector = vectorizer.transform([email_text]).toarray()
    
    rf_pred = rf_model.predict(email_vector)[0]
    sgd_pred = sgd_model.predict(email_vector)[0]

    response = {
        "RandomForest": "Phishing" if rf_pred == 1 else "Not Phishing",
        "SGDClassifier": "Phishing" if sgd_pred == 1 else "Not Phishing"
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
