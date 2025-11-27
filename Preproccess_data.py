import pickle  # Import pickle for serializing the processed data and vectorizer to disk.
import pandas as pd  # Import pandas for efficient data manipulation and CSV reading.
from sklearn.feature_extraction.text import TfidfVectorizer  # Import TF-IDF Vectorizer to convert text data into numerical vectors.

def preprocess_data(raw_data_file, preprocessed_file):
    """
    Reads raw email data, preprocesses it, and saves the features, labels, and vectorizer.

    Args:
        raw_data_file (str): Path to the input CSV file containing raw email data.
        preprocessed_file (str): Path where the processed artifacts (X, y, vectorizer) will be saved.
    """
    
    # ---------------------------------------------------------
    # Data Loading
    # ---------------------------------------------------------
    # Read the raw CSV file into a pandas DataFrame.
    # The CSV is expected to have headers, specifically 'email_text' and 'label'.
    df = pd.read_csv(raw_data_file)

    # ---------------------------------------------------------
    # Feature Extraction
    # ---------------------------------------------------------
    # Extract the 'email_text' column and convert it to a list of strings.
    # .astype(str) ensures all entries are treated as strings, handling potential missing values or non-string types.
    emails = df['email_text'].astype(str).tolist()
    
    # Extract the 'label' column (0 for safe, 1 for phishing) as a list.
    labels = df['label'].tolist()

    # ---------------------------------------------------------
    # Text Vectorization (TF-IDF)
    # ---------------------------------------------------------
    # Initialize the TF-IDF Vectorizer.
    # max_features=5000: Limit the vocabulary to the top 5000 most frequent words to reduce dimensionality.
    # stop_words='english': Remove common English words (e.g., 'the', 'is') that add little predictive value.
    vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
    
    # Fit the vectorizer to the email text (learn vocabulary) and transform the text into a matrix of TF-IDF features.
    # .toarray() converts the sparse matrix to a dense numpy array.
    X = vectorizer.fit_transform(emails).toarray()  # X represents the feature matrix.

    # ---------------------------------------------------------
    # Artifact Serialization
    # ---------------------------------------------------------
    # Save the processed features (X), labels (labels), and the fitted vectorizer to a pickle file.
    # Saving the vectorizer is crucial so we can transform new, unseen emails in the same way during prediction.
    with open(preprocessed_file, "wb") as f:
        pickle.dump((X, labels, vectorizer), f)

    print(f"Preprocessed data saved to {preprocessed_file}")

# Entry point of the script.
if __name__ == "__main__":
    # Execute the preprocessing pipeline.
    preprocess_data(
        raw_data_file="Phishing_validation_emails.csv",  # Input raw data file.
        preprocessed_file="data/preprocessed_data.pkl"   # Output file for processed data.
    )
