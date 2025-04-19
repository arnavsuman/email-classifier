---
title: Email Classifier API
emoji: 📧
colorFrom: blue
colorTo: indigo
sdk: docker
app_file: app.py
pinned: false
---
# Email Classifier API

## Features
- Classifies support emails into categories (e.g., Billing, Technical Support)
- Masks sensitive PII/PCI information using regex and SpaCy (non-LLM)
- Exposes a POST API endpoint with strict JSON response

HUGGING FACE URL  https://arnav-suman-email-classifier.hf.space/classify
## PIPELINE

           [ Raw Email ]
                 ↓
     ┌──────────────────────┐
     │  PII Masking Module  │ ← Regex + SpaCy
     └──────────────────────┘
                 ↓
     ┌──────────────────────┐
     │ Classification Model │ ← ML/DL/LLM
     └──────────────────────┘
                 ↓
     ┌────────────────────────────┐
     │ Final Output Construction  │
     └────────────────────────────┘

## APPROACH

1. PII/PCI Masking (Preprocessing)

Replace sensitive info (e.g., name, email, phone) with [entity_type].

Approach:
Use Regex for:

Email ([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)

Phone Numbers

Credit/Debit card numbers, CVV, expiry date

Aadhar number (12-digit)

Use SpaCy NER (non-LLM) for names, DOBs, etc.

Store original values and positions for demaskin



2. Email Classification (ML/DL/LLM)
Goal: Classify emails into categories like Billing, Tech Support, etc.
Options:

Traditional ML: TF-IDF + SVM
Quick to train and deploy, good baseline.

Option 2 DL: Fine-tune BERT (or use pre-trained distilbert-base-uncased)
Best performance for language understanding.



3. API Development
Use FastAPI for clean structure + async support.

Endpoint: /classify
Method: POST

INPUT 
{
  "input_email_body": "Hello, my name is John, and my email is johndoe@example.com"
}
OUTPUT
{
  "input_email_body": "Hello, my name is John, and my email is johndoe@example.com",
  "list_of_masked_entities": [
    {
      "position": [18, 22 ],
      "classification": "full_name",
      "entity": "John"
    },
    {
      "position": [40, 59],
      "classification": "email",
      "entity": "johndoe@example.com"
    }
  ],
  "masked_email": "Hello, my name is [full_name] and my email is [email]",
  "category_of_the_email": "Technical Support"
}

## TESTING
Also included is a test_api.py that does following:
    Handles edge cases gracefully
    Provides fallback category in unusual or empty inputs
    Follows strict response structure
TO RUN IT:

```bash
python -m spacy download en_core_web_sm

python test_api.py
```

## Setup Instructions

```bash
# 1. Clone the repo
git clone <your_repo_link>
cd email_classifier_project

# 2. Create environment & install dependencies
pip install -r requirements.txt

# 3. Download SpaCy model
python -m spacy download en_core_web_sm

# 4. If want to train your own model otherwise skip as pretrained model (by me) is included  
python models.py

# 5. Run the API
uvicorn app:app --reload


