import pickle

def predict_email(email_text, vectorizer_file, rf_model_file=None, sgd_model_file=None, use_rf=True, use_sgd=False):
    """
    Predict phishing/not phishing for a given email text.
    Can use Random Forest and/or SGDClassifier models.
    Returns dict of predictions.
    """

    # Load vectorizer from pickle (same as preprocessing)
    with open(vectorizer_file, "rb") as f:
        _, _, vectorizer = pickle.load(f)

    # Vectorize input email
    email_vector = vectorizer.transform([email_text]).toarray()

    predictions = {}

    if use_rf and rf_model_file is not None:
        with open(rf_model_file, "rb") as f:
            rf_model = pickle.load(f)
        rf_pred = rf_model.predict(email_vector)
        predictions['RandomForest'] = "Phishing" if rf_pred[0] == 1 else "Not Phishing"

    if use_sgd and sgd_model_file is not None:
        with open(sgd_model_file, "rb") as f:
            sgd_model = pickle.load(f)
        sgd_pred = sgd_model.predict(email_vector)
        predictions['SGDClassifier'] = "Phishing" if sgd_pred[0] == 1 else "Not Phishing"

    return predictions


if __name__ == "__main__":
    #email = "Your account has been compromised. Please reset your password."
    email = "regarding the meeting we had last week, please tell us what you think about the proposal."
    preds = predict_email(email,
                          vectorizer_file="data/preprocessed_data.pkl",
                          rf_model_file="models/phishing_rf.pkl",
                          sgd_model_file="models/phishing_sgd.pkl",
                          use_rf=True,
                          use_sgd=True)
    for model_name, result in preds.items():
        print(f"{model_name} prediction: {result}")
