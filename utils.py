import re
import spacy

nlp = spacy.load("en_core_web_sm")

# Regex patterns for detecting PII
patterns = {
    "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    "phone_number": r"\b\d{10}\b",
    "aadhar_num": r"\b\d{4}\s?\d{4}\s?\d{4}\b",
    "credit_debit_no": r"\b(?:\d[ -]*?){13,16}\b",
    "cvv_no": r"\b\d{3}\b",
    "expiry_no": r"\b(0[1-9]|1[0-2])\/\d{2,4}\b",
    "dob": r"\b\d{2}[\/.-]\d{2}[\/.-]\d{4}\b"
}


def mask_pii(text):
    entities = []
    masked_text = text

    # Regex-based masking
    for label, pattern in patterns.items():
        for match in re.finditer(pattern, text):
            span = match.span()
            original = match.group()

            entities.append({
                "position": list(span),
                "classification": label,
                "entity": original
            })

            masked_text = masked_text.replace(original, f"[{label}]")

    # SpaCy-based name detection
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            start, end = ent.start_char, ent.end_char

            entities.append({
                "position": [start, end],
                "classification": "full_name",
                "entity": ent.text
            })

            masked_text = masked_text.replace(ent.text, "[full_name]")

    return masked_text, entities
