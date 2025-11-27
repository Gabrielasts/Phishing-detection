#!/bin/bash

# Script to install dependencies, run tests, and check code quality

pip install -r requirements.txt

# Run tests (assuming pytest or similar) - add your test command here
pytest

# Run linting (add your linting tool command if available)
# e.g., flake8 or pylint
# flake8 .

# Run the app (optional for local testing)
# python BackendRest.py


echo "Setup and test script finished."