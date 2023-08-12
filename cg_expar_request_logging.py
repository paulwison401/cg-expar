import os
from flask import Flask, request, jsonify
import pdfplumber
import spacy
import requests
from spacy.util import is_package
from io import BytesIO
import logging
from urllib.parse import urlparse

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Check if the language model is downloaded
if not is_package('en_core_web_sm'):
    try:
        spacy.cli.download('en_core_web_sm')
    except Exception as e:
        logging.error(f"Failed to download language model: {e}")
        raise

nlp = spacy.load("en_core_web_sm")

def extract_information(text):
    # Process the text with spaCy
    doc = nlp(text)
    
    # ... rest of the function remains the same ...

@app.route("/extract_and_summarize", methods=["POST"])
def extract_and_summarize():
    # Log the received request data
    logging.info(f"Received data: {request.data}")
    
    try:
        json_data = request.get_json(force=True)
        pdf_url = json_data.get("pdf_url")
    except Exception as e:
        logging.error(f"Failed to get JSON data: {e}")
        return jsonify({"error": "Invalid JSON data"}), 400

    # ... rest of the function remains the same ...

if __name__ == "__main__":
    app.run(debug=False, host=os.getenv('HOST', '0.0.0.0'), port=int(os.getenv('PORT', 5000)))
