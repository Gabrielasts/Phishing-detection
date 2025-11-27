# Gmail Phishing Detector

A machine learning-based system to detect phishing emails directly within Gmail. This project consists of a Python backend API and a Chrome Extension.

## Project Structure

- **Backend**: `BackendRest.py` (Flask API)
- **ML Training**: `TeachMLM.py` (Trains Random Forest & SGD models)
- **Preprocessing**: `Preproccess_data.py` (Data cleaning & vectorization)
- **Chrome Extension**: `manifest.json`, `background.js`, `content.js`
- **Data**: `data/` (Contains preprocessed data)
- **Models**: `models/` (Contains trained models)

## Setup Instructions

### 1. Python Environment Setup

Ensure you have Python 3.10+ installed.

1.  Clone the repository.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### 2. Train Models (Optional)

If you need to retrain the models:

1.  Place your dataset in the project folder (e.g., `Phishing_validation_emails.csv`).
2.  Run preprocessing:
    ```bash
    python Preproccess_data.py
    ```
3.  Train the models:
    ```bash
    python TeachMLM.py
    ```

### 3. Run the Backend Server

The Chrome extension communicates with this local server to get predictions.

```bash
python BackendRest.py
```

The server will start on `http://localhost:5000`.

### 4. Install Chrome Extension

1.  Open Chrome and navigate to `chrome://extensions/`.
2.  Enable **Developer mode** (top right).
3.  Click **Load unpacked**.
4.  Select the project folder (where `manifest.json` is located).

## Usage

1.  Ensure the backend server is running.
2.  Open Gmail in your browser.
3.  The extension will automatically scan emails and alert you if a phishing attempt is detected.
