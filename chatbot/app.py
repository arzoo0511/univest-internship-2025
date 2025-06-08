from flask import Flask, render_template, request, jsonify
import spacy
import json
import os

app = Flask(__name__)

# Load spaCy NER model
try:
    nlp = spacy.load("en_core_web_sm")  # Use 'ner_model' if you've trained your own
except:
    raise Exception("SpaCy model not found. Make sure you installed and downloaded it using: python -m spacy download en_core_web_sm")

# Load stock/company data from JSON file
if not os.path.exists("companies.json"):
    raise FileNotFoundError("Missing 'companies.json'. Please ensure it is in the same directory as app.py")

with open("companies.json", "r", encoding="utf-8") as f:
    stock_data = json.load(f)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/get_response', methods=["POST"])
def get_response():
    user_input = request.json.get("message", "")
    if not user_input:
        return jsonify({"response": "Please enter a message."})

    doc = nlp(user_input)

    # Try to find a company name in the input
    company = None
    for ent in doc.ents:
        if ent.label_ in ["ORG", "GPE", "PRODUCT"]:
            company = ent.text.strip().title()
            break

    # If spaCy fails to find company, try simple keyword matching
    if not company:
        for name in stock_data:
            if name.lower() in user_input.lower():
                company = name
                break

    if not company:
        return jsonify({"response": "Sorry, I couldn't find the company in your message."})

    if company not in stock_data:
        return jsonify({"response": f"Sorry, I don't have data on {company}."})

    # Build response
    info = stock_data[company]
    response = f"**About {company}:** {info.get('about', 'No description available.')}\n\n"

    if "financials" in info:
        response += "**Financials:**\n"
        for key, val in info["financials"].items():
            response += f"- {key}: {val}\n"

    if "pros" in info:
        response += f"\n**Pros:** {info['pros']}"
    if "cons" in info:
        response += f"\n**Cons:** {info['cons']}"

    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
