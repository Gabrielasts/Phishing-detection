import pickle  # Import the pickle module to serialize and deserialize Python objects (e.g., saving/loading models).
from sklearn.ensemble import RandomForestClassifier  # Import the Random Forest Classifier, a robust ensemble learning method.
from sklearn.linear_model import SGDClassifier  # Import the SGD Classifier, efficient for large-scale and incremental learning.
from sklearn.model_selection import train_test_split  # Import utility to split datasets into training and testing subsets.
from sklearn.metrics import accuracy_score  # Import metric to evaluate model performance by calculating accuracy.

def train_or_update_model(preprocessed_file,
                          rf_model_file, sgd_model_file,
                          use_rf=True, rebuild_rf=False,
                          use_sgd=False, append_sgd=False):
    """
    Orchestrates the training and updating of machine learning models for phishing detection.

    Args:
        preprocessed_file (str): Path to the pickled file containing preprocessed features (X), labels (y), and vectorizer.
        rf_model_file (str): Path where the Random Forest model is saved or loaded from.
        sgd_model_file (str): Path where the SGD model is saved or loaded from.
        use_rf (bool): Flag to determine if the Random Forest model should be processed.
        rebuild_rf (bool): Flag to force retraining of the Random Forest model from scratch.
        use_sgd (bool): Flag to determine if the SGD model should be processed.
        append_sgd (bool): Flag to enable incremental learning (partial_fit) for the SGD model.
    """

    # Open the preprocessed data file in binary read mode.
    with open(preprocessed_file, "rb") as f:
        # Load the features matrix (X), target labels (y), and the fitted vectorizer.
        X, y, vectorizer = pickle.load(f)

    # ---------------------------------------------------------
    # Random Forest Model Logic
    # ---------------------------------------------------------
    if use_rf:
        # Check if the user requested to rebuild the Random Forest model entirely.
        if rebuild_rf:
            # Split the dataset: 80% for training and 20% for testing to validate performance.
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Initialize the Random Forest Classifier with a fixed random state for reproducible results.
            rf_model = RandomForestClassifier(random_state=42)
            
            # Fit the model on the training data.
            rf_model.fit(X_train, y_train)
            
            # Generate predictions on the unseen test set.
            y_pred = rf_model.predict(X_test)
            
            # Calculate accuracy by comparing predictions to actual labels.
            accuracy = accuracy_score(y_test, y_pred)
            print(f"[Random Forest] Rebuilt Model Accuracy: {accuracy:.3f}")

            # Save the trained Random Forest model to disk for future use.
            with open(rf_model_file, "wb") as f:
                pickle.dump(rf_model, f)
            print(f"Random Forest model rebuilt and saved to {rf_model_file}")
        else:
            # Attempt to load an existing Random Forest model if rebuild is not requested.
            try:
                with open(rf_model_file, "rb") as f:
                    rf_model = pickle.load(f)
                print("[Random Forest] Existing model loaded. No rebuild flag given.")
            except FileNotFoundError:
                # If no existing model is found, train a new one on the full dataset.
                rf_model = RandomForestClassifier(random_state=42)
                rf_model.fit(X, y)
                
                # Save the newly trained model.
                with open(rf_model_file, "wb") as f:
                    pickle.dump(rf_model, f)
                print(f"[Random Forest] Model trained on full data and saved to {rf_model_file}")

    # ---------------------------------------------------------
    # SGD Classifier Model Logic (Incremental Learning)
    # ---------------------------------------------------------
    if use_sgd:
        # Attempt to load an existing SGD model to continue training (incremental learning).
        try:
            with open(sgd_model_file, "rb") as f:
                sgd_model = pickle.load(f)
            print("[SGDClassifier] Existing model loaded.")
        except FileNotFoundError:
            # If no model exists, initialize a new SGDClassifier.
            # loss='log_loss' gives logistic regression (probabilistic output).
            sgd_model = SGDClassifier(loss="log_loss", max_iter=1000, tol=1e-3, random_state=42)
            
            # Perform the first batch of training. 
            # 'classes' must be provided on the first call to partial_fit.
            sgd_model.partial_fit(X, y, classes=[0, 1])
            
            # Save the initialized model.
            with open(sgd_model_file, "wb") as f:
                pickle.dump(sgd_model, f)
            print("[SGDClassifier] Model trained on full data and saved.")
            return  # Exit early as initial training is complete.

        # If the model exists and append mode is on, update it with new data.
        if append_sgd:
            # Update the model weights using the new data batch.
            sgd_model.partial_fit(X, y)
            
            # Save the updated model state.
            with open(sgd_model_file, "wb") as f:
                pickle.dump(sgd_model, f)
            print("[SGDClassifier] Model incrementally updated and saved.")

        # Evaluate the updated model on the current dataset.
        y_pred = sgd_model.predict(X)
        accuracy = accuracy_score(y, y_pred)
        print(f"[SGDClassifier] Model Accuracy on updated data: {accuracy:.3f}")

# Entry point of the script.
if __name__ == "__main__":
    # Execute the training pipeline with specific configuration parameters.
    train_or_update_model(
        preprocessed_file="data/preprocessed_data.pkl",  # Source of vectorized data.
        rf_model_file="models/phishing_rf.pkl",          # Destination for Random Forest model.
        sgd_model_file="models/phishing_sgd.pkl",        # Destination for SGD model.
        use_rf=True,       # Enable Random Forest processing.
        rebuild_rf=True,   # Force a complete retrain of Random Forest.
        use_sgd=True,      # Enable SGD processing.
        append_sgd=True    # Allow incremental updates to SGD.
    )
