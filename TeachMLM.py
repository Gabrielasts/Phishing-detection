import pickle  # Import the pickle module for serializing and de-serializing Python object structures.
from sklearn.ensemble import RandomForestClassifier  # Import the Random Forest classifier from scikit-learn.
from sklearn.linear_model import SGDClassifier  # Import the Stochastic Gradient Descent classifier for incremental learning.
from sklearn.model_selection import train_test_split  # Import function to split data into training and testing sets.
from sklearn.metrics import accuracy_score  # Import function to calculate the accuracy of a model.

# Define a function to train or update machine learning models.
def train_or_update_model(preprocessed_file,
                          rf_model_file, sgd_model_file,
                          use_rf=True, rebuild_rf=False,  # Flags to control Random Forest model training.
                          use_sgd=False, append_sgd=False):  # Flags to control SGD model training.
    """
    Train or rebuild Random Forest model, or train/append SGDClassifier incrementally,
    depending on flags provided. Evaluates models after training.
    """

    # Load preprocessed data (features, labels, and the vectorizer) from a pickle file.
    with open(preprocessed_file, "rb") as f:  # Open the file in binary read mode.
        X, y, vectorizer = pickle.load(f)  # Unpickle the data into features (X), labels (y), and the vectorizer.

    # Check if the Random Forest model should be used/trained.
    if use_rf:
        # Check if the Random Forest model should be rebuilt from scratch.
        if rebuild_rf:
            # Split the data into training (80%) and testing (20%) sets for evaluation.
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            # Initialize a new Random Forest classifier with a fixed random state for reproducibility.
            rf_model = RandomForestClassifier(random_state=42)
            # Train the model on the training data.
            rf_model.fit(X_train, y_train)
            # Make predictions on the test data to evaluate the newly trained model.
            y_pred = rf_model.predict(X_test)
            # Calculate the accuracy of the model on the test set.
            accuracy = accuracy_score(y_test, y_pred)
            # Print the accuracy of the rebuilt model.
            print(f"[Random Forest] Rebuilt Model Accuracy: {accuracy:.3f}")

            # Save the newly trained Random Forest model to a file.
            with open(rf_model_file, "wb") as f:  # Open the file in binary write mode.
                pickle.dump(rf_model, f)  # Serialize and save the model object.
            print(f"Random Forest model rebuilt and saved to {rf_model_file}")  # Confirm saving.
        else:
            # If not rebuilding, try to load an existing model.
            try:
                with open(rf_model_file, "rb") as f:  # Open the model file in binary read mode.
                    rf_model = pickle.load(f)  # Load the existing model.
                print("[Random Forest] Existing model loaded. No rebuild flag given.")  # Inform the user.
            except FileNotFoundError:  # If the model file doesn't exist, train a new one.
                rf_model = RandomForestClassifier(random_state=42)  # Initialize a new classifier.
                rf_model.fit(X, y)  # Train the model on the entire dataset.
                with open(rf_model_file, "wb") as f:  # Open the model file in binary write mode.
                    pickle.dump(rf_model, f)  # Save the newly trained model.
                print(f"[Random Forest] Model trained on full data and saved to {rf_model_file}")  # Confirm saving.

    # Check if the SGD classifier should be used/trained.
    if use_sgd:
        # Try to load an existing SGD model. SGD supports incremental learning.
        try:
            with open(sgd_model_file, "rb") as f:  # Open the model file in binary read mode.
                sgd_model = pickle.load(f)  # Load the existing model.
            print("[SGDClassifier] Existing model loaded.")  # Inform the user.
        except FileNotFoundError:  # If the model file doesn't exist, create and train a new one.
            # Initialize a new SGD classifier. `loss="log_loss"` enables probability estimates.
            sgd_model = SGDClassifier(loss="log_loss", max_iter=1000, tol=1e-3, random_state=42)
            # Perform an initial training. `partial_fit` requires the list of all possible classes on the first call.
            sgd_model.partial_fit(X, y, classes=[0, 1])
            with open(sgd_model_file, "wb") as f:  # Open the model file in binary write mode.
                pickle.dump(sgd_model, f)  # Save the newly trained model.
            print("[SGDClassifier] Model trained on full data and saved.")  # Confirm saving.
            return  # Exit the function since the initial training is complete.

        # If the `append_sgd` flag is set, update the existing model with the new data.
        if append_sgd:
            # Update the model incrementally using `partial_fit` without the classes argument.
            sgd_model.partial_fit(X, y)
            with open(sgd_model_file, "wb") as f:  # Open the file in binary write mode to save the updated model.
                pickle.dump(sgd_model, f)  # Save the updated model.
            print("[SGDClassifier] Model incrementally updated and saved.")  # Confirm the update.

        # Evaluate the SGD model's performance on the entire dataset (X).
        y_pred = sgd_model.predict(X)  # Make predictions on the full dataset.
        accuracy = accuracy_score(y, y_pred)  # Calculate the accuracy.
        print(f"[SGDClassifier] Model Accuracy on updated data: {accuracy:.3f}")  # Print the accuracy.

# This block executes only when the script is run directly (not imported as a module).
if __name__ == "__main__":
    # Call the main function to train or update the models.
    train_or_update_model(
        preprocessed_file="data/preprocessed_data.pkl",  # Path to the preprocessed data file.
        rf_model_file="models/phishing_rf.pkl",  # Path to save/load the Random Forest model.
        sgd_model_file="models/phishing_sgd.pkl",  # Path to save/load the SGD model.
        use_rf=True,  # Enable training/loading for the Random Forest model.
        rebuild_rf=True,  # Force a rebuild of the Random Forest model.
        use_sgd=True,  # Enable training/loading for the SGD model.
        append_sgd=True  # Incrementally update the SGD model if it exists.
    )
