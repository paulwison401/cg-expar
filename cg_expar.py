from flask import Flask, request, jsonify
import pdfplumber
import spacy
import requests
from io import BytesIO

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

def extract_information(text):
    # Process the text with spaCy
    doc = nlp(text)

    # Initialize variables to store extracted information
    name = ""
    credit_score = ""
    open_accounts = ""
    accounts_ever_late = ""

    # Find the entity with the label "PERSON"
    for entity in doc.ents:
        if entity.label_ == "PERSON":
            name = entity.text
            break

    # Extract Credit Score
    for sent in doc.sents:
        if "FICO" in sent.text and "Score" in sent.text:
            credit_score = sent.text.split("Score")[-1].strip()
            break

    # Extract Open Accounts
    for sent in doc.sents:
        if "Open accounts" in sent.text:
            open_accounts = sent.text.split(":")[-1].strip()
            break

    # Extract Accounts Ever Late
    for sent in doc.sents:
        if "Accounts ever late" in sent.text:
            accounts_ever_late = sent.text.split(":")[-1].strip()
            break

    # Return the extracted information as a dictionary
    return {"name": name, "credit_score": credit_score, "open_accounts": open_accounts, "accounts_ever_late": accounts_ever_late}

@app.route("/extract_and_summarize", methods=["POST"])
def extract_and_summarize():
    pdf_url = request.json.get("pdf_url")
    if not pdf_url:
        return jsonify({"error": "No URL provided"}), 400

    response = requests.get(pdf_url)
    pdf_file = BytesIO(response.content)

    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()

    info = extract_information(text)

    return jsonify(info)

if __name__ == "__main__":
    app.run(debug=True)
