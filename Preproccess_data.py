import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

def preprocess_data(raw_data_file, preprocessed_file):
    """
    Load raw dataset (CSV or similar), preprocess, vectorize text, save features and labels for training.
    Assumes CSV with columns 'email_text' and 'label' (1 for phishing, 0 for not).
    """
    # Load raw data
    df = pd.read_csv(raw_data_file)

    # Extract email text and labels
    emails = df['email_text'].astype(str).tolist()
    labels = df['label'].tolist()

    # Vectorize email text with TF-IDF (learn vocabulary here)
    vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
    X = vectorizer.fit_transform(emails).toarray()  # Features matrix

    # Save preprocessed data: features (X), labels (y), and vectorizer
    with open(preprocessed_file, "wb") as f:
        pickle.dump((X, labels, vectorizer), f)

    print(f"Preprocessed data saved to {preprocessed_file}")

if __name__ == "__main__":
    preprocess_data("Phishing_validation_emails.csv", "data/preprocessed_data.pkl")
