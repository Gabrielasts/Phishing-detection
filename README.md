# Gmail Phishing Detector

![Python](https://img.shields.io/badge/python-3.10+-blue?style=flat&logo=python&logoColor=white) ![Flask](https://img.shields.io/badge/flask-1.1.2-orange?style=flat&logo=flask&logoColor=white) ![GitHub](https://img.shields.io/badge/github-repo-black?style=flat&logo=github&logoColor=white) ![License](https://img.shields.io/badge/license-MIT-green?style=flat)

---

A machine learning-based system to detect phishing emails directly within Gmail. This project consists of a Python backend API and a Chrome Extension that scans emails and alerts users automatically.

## Features

- Real-time phishing detection inside Gmail
- Machine learning models trained with Random Forest and SGD
- RESTful Flask backend for predictions
- Chrome Extension with content and background scripts

## Tech Stack

- Python 3.10+
- Flask API
- Scikit-learn for ML
- JavaScript (Chrome Extension)

## Project Structure

- **Backend**: `BackendRest.py` (Flask API)
- **ML Training**: `TeachMLM.py` (Trains Random Forest & SGD models)
- **Preprocessing**: `Preproccess_data.py` (Data cleaning & vectorization)
- **Chrome Extension**: `manifest.json`, `background.js`, `content.js`
- **Data**: `data/` (Contains preprocessed data)
- **Models**: `models/` (Contains trained models)

## Setup Instructions

### Prerequisites

- Python 3.10 or later installed
- Chrome browser
- Git installed

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/the3y3-code/Phishing-detection.git
    cd Phishing-detection
    ```
2. Install Python dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### Train Models (Optional)

1. Place your dataset CSV file (`Phishing_validation_emails.csv`) in the project root.
2. Run preprocessing script:

    ```bash
    python Preproccess_data.py
    ```
3. Run training script:

    ```bash
    python TeachMLM.py
    ```

### Run Backend Server

Run the backend Flask API:

```bash
python BackendRest.py
```

Access the server at `http://localhost:5000`.

### Install Chrome Extension

1. Open Chrome and navigate to `chrome://extensions/`.
2. Enable **Developer mode**.
3. Click **Load unpacked** and select this repo directory.

## Usage

- Start backend server.
- Open Gmail; the extension will scan emails automatically.

## Running Tests

Add tests if available, and run them with:

```bash
pytest
```

## Contributing

Contributions are welcome! Please fork this repo, make changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Created by the3y3-code. Feel free to reach out via GitHub.
