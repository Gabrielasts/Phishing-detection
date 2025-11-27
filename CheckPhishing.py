import pickle  # Import pickle to deserialize the vectorizer and machine learning models.

def predict_email(email_text, vectorizer_file, rf_model_file=None, sgd_model_file=None, use_rf=True, use_sgd=False):
    """
    Analyzes an email text and predicts whether it is a phishing attempt using specified models.

    Args:
        email_text (str): The content of the email to be analyzed.
        vectorizer_file (str): Path to the pickled TF-IDF vectorizer file.
        rf_model_file (str, optional): Path to the Random Forest model file. Required if use_rf is True.
        sgd_model_file (str, optional): Path to the SGD model file. Required if use_sgd is True.
        use_rf (bool): Flag to enable prediction using the Random Forest model.
        use_sgd (bool): Flag to enable prediction using the SGD model.

    Returns:
        dict: A dictionary containing predictions from the enabled models.
              Example: {'RandomForest': 'Phishing', 'SGDClassifier': 'Not Phishing'}
    """

    # ---------------------------------------------------------
    # Vectorizer Loading
    # ---------------------------------------------------------
    # Load the pre-fitted TF-IDF vectorizer.
    # It is crucial to use the exact same vectorizer that was used during training
    # to ensure the feature space (vocabulary mapping) remains consistent.
    with open(vectorizer_file, "rb") as f:
        _, _, vectorizer = pickle.load(f)

    # ---------------------------------------------------------
    # Feature Transformation
    # ---------------------------------------------------------
    # Transform the input email text into a numerical feature vector.
    # The input must be a list, even for a single email.
    # .toarray() converts the sparse matrix representation to a dense array for model compatibility.
    email_vector = vectorizer.transform([email_text]).toarray()

    predictions = {}

    # ---------------------------------------------------------
    # Random Forest Prediction
    # ---------------------------------------------------------
    if use_rf and rf_model_file is not None:
        # Load the Random Forest model from disk.
        with open(rf_model_file, "rb") as f:
            rf_model = pickle.load(f)
        
        # Generate prediction. The result is an array (e.g., [1]), so we take the first element.
        rf_pred = rf_model.predict(email_vector)
        
        # Map the numerical prediction (1/0) to a human-readable string.
        predictions['RandomForest'] = "Phishing" if rf_pred[0] == 1 else "Not Phishing"

    # ---------------------------------------------------------
    # SGD Classifier Prediction
    # ---------------------------------------------------------
    if use_sgd and sgd_model_file is not None:
        # Load the SGD model from disk.
        with open(sgd_model_file, "rb") as f:
            sgd_model = pickle.load(f)
        
        # Generate prediction.
        sgd_pred = sgd_model.predict(email_vector)
        
        # Map the numerical prediction to a human-readable string.
        predictions['SGDClassifier'] = "Phishing" if sgd_pred[0] == 1 else "Not Phishing"

    return predictions


# ---------------------------------------------------------
# Script Entry Point (for manual testing)
# ---------------------------------------------------------
if __name__ == "__main__":
    # Example email text to test the prediction logic.
    # email = "Your account has been compromised. Please reset your password."
    email = "regarding the meeting we had last week, please tell us what you think about the proposal."
    
    # Call the prediction function with paths to the artifacts.
    preds = predict_email(email,
                          vectorizer_file="data/preprocessed_data.pkl",
                          rf_model_file="models/phishing_rf.pkl",
                          sgd_model_file="models/phishing_sgd.pkl",
                          use_rf=True,
                          use_sgd=True)
    
    # Print the results for each model.
    for model_name, result in preds.items():
        print(f"{model_name} prediction: {result}")
