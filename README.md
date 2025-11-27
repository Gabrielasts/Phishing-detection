# Gmail Phishing Detector

![Python](https://img.shields.io/badge/python-3.10+-blue.svg?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/flask-2.0+-orange.svg?style=flat&logo=flask&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat)
![Chrome Extension](https://img.shields.io/badge/chrome-extension-yellow.svg?style=flat&logo=googlechrome&logoColor=white)
![Machine Learning](https://img.shields.io/badge/ML-scikit--learn-F7931E.svg?style=flat&logo=scikit-learn&logoColor=white)
![Status](https://img.shields.io/badge/status-active-success.svg?style=flat)
![Contributions](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)

---

A machine learning-based system to detect phishing emails directly within Gmail. This project consists of a Python backend API and a Chrome Extension that scans emails in real-time and alerts users automatically.

## Features

- 🛡️ **Real-time phishing detection** inside Gmail
- 🤖 **Machine learning models** trained with Random Forest and SGD classifiers
- 🚀 **RESTful Flask backend** for predictions
- 🌐 **Chrome Extension** with content and background scripts
- 📊 **Data preprocessing** and feature extraction pipeline
- ⚡ **Fast response times** for email scanning

## Tech Stack

- **Python** 3.10+
- **Flask** - RESTful API framework
- **Scikit-learn** - Machine learning library
- **JavaScript** - Chrome Extension
- **Random Forest & SGD** - ML algorithms

## Project Structure

```
Phishing-detection/
├── BackendRest.py              # Flask API server
├── TeachMLM.py                 # ML model training script
├── Preproccess_data.py         # Data cleaning & vectorization
├── manifest.json               # Chrome extension manifest
├── background.js               # Extension background script
├── content.js                  # Extension content script
├── data/                       # Preprocessed datasets
├── models/                     # Trained ML models
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
└── LICENSE                     # MIT License
```

## Prerequisites

- Python 3.10 or later
- Chrome browser
- Git
- pip (Python package manager)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/the3y3-code/Phishing-detection.git
cd Phishing-detection
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables (Optional)

Copy the example environment file and customize if needed:

```bash
cp .env.example .env
```

## Usage

### Train Models (Optional)

If you want to retrain the models with your own dataset:

1. Place your dataset CSV file (e.g., `Phishing_validation_emails.csv`) in the project root.
2. Run preprocessing:

```bash
python Preproccess_data.py
```

3. Train the models:

```bash
python TeachMLM.py
```

### Run the Backend Server

Start the Flask API server:

```bash
python BackendRest.py
```

The server will be accessible at `http://localhost:5000`.

### Install Chrome Extension

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable **Developer mode** (toggle in top right)
3. Click **Load unpacked**
4. Select the `Phishing-detection` project directory

### Using the Extension

1. Ensure the backend server is running
2. Open Gmail in your browser
3. The extension will automatically scan incoming emails
4. Alerts will appear if phishing attempts are detected

## Running Tests

To run tests (if implemented):

```bash
pytest tests/
```

## API Endpoints

### POST /predict

Predicts if an email is phishing or legitimate.

**Request:**
```json
{
  "email_content": "Your email text here"
}
```

**Response:**
```json
{
  "prediction": "phishing" | "legitimate",
  "confidence": 0.95
}
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and development process.

## Roadmap

- [ ] Add deep learning models (LSTM, BERT)
- [ ] Support for multiple email providers
- [ ] Mobile app version
- [ ] Real-time threat intelligence integration
- [ ] Multi-language support

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Scikit-learn community for ML tools
- Flask framework contributors
- Chrome Extensions documentation

## Contact

**the3y3-code** - [GitHub Profile](https://github.com/the3y3-code)

Project Link: [https://github.com/the3y3-code/Phishing-detection](https://github.com/the3y3-code/Phishing-detection)

---

⭐ If you find this project useful, please consider giving it a star!
