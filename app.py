from flask import Flask, request, jsonify
from flasgger import Swagger
import joblib
import spacy
import re

# load scikit-learn classifier
model = joblib.load("model/document_classifier.pkl")

# load spaCy model
nlp = spacy.load("custom_ner_model")  # your custom trained model

app = Flask(__name__)
swagger = Swagger(app)

def hybrid_extract(text, predicted_class):
    doc = nlp(text)
    spaCy_entities = {}
    for ent in doc.ents:
        spaCy_entities.setdefault(ent.label_, []).append(ent.text)

    regex_entities = {}

    if predicted_class == "beneficiary_change":
        pol = re.search(r'policy\s+number\s+(\d+)', text, re.I)
        if pol:
            regex_entities["policy_number"] = pol.group(1)

        ben = re.search(r'(?:beneficiary\s+)?(?:to|with)\s+(?:my\s+)?(?:wife|husband|son|daughter)?\s*([A-Z][a-z]+\s+[A-Z][a-z]+)', text, re.I)
        if ben:
            regex_entities["beneficiary_name"] = ben.group(1)

    if predicted_class == "address_change":
        addr = re.search(r'(\d+\s+[\w\s]+(?:Street|St|Road|Rd|Lane|Ln|Avenue|Ave|Drive|Dr))', text, re.I)
        if addr:
            regex_entities["new_address"] = addr.group(1).strip()

        date = re.search(r'\beffective\s+(?:from\s+)?(?:\w+\s+\d{4}|next\s+\w+|immediately)', text, re.I)
        if date:
            regex_entities["effective_date"] = date.group(0)

    # add phone/email
    phone = re.search(r'\+?\d[\d\s-]{7,}', text)
    if phone:
        regex_entities["phone_number"] = phone.group(0)

    email = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', text)
    if email:
        regex_entities["email"] = email.group(0)

    return predicted_class, regex_entities

@app.route("/extract",  methods=["GET", "POST"])
def extract():
    """
    Text Classification and Entity Extraction
    ---
    parameters:
      - name: text
        in: body
        required: true
        schema:
          type: object
          properties:
            text:
              type: string
              example: "Please update my address to 123 Main Street effective next month"
    responses:
      200:
        description: Successful response
        schema:
          type: object
          properties:
            predicted_class:
              type: string
            entities:
              type: object
    """
    data = request.get_json()
    text = data.get("text")

    # predict the class using scikit-learn
    predicted_class = model.predict([text])[0]

    # extract entities with spaCy + regex hybrid
    predicted_class, entities = hybrid_extract(text, predicted_class)

    return jsonify({"predicted_class": predicted_class, "entities": entities})

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0", port=5000)
