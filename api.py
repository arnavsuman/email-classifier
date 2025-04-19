from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import joblib
import traceback

from utils import mask_pii

# Load model once
model = joblib.load("model_checkpoints/tfidf_svm_model.pkl")

router = APIRouter()


class EmailRequest(BaseModel):
    input_email_body: str


@router.post("/classify")
def classify_email(req: EmailRequest):
    try:
        raw_email = req.input_email_body.strip()

        if not raw_email:
            return JSONResponse(
                content={
                    "input_email_body": "",
                    "list_of_masked_entities": [],
                    "masked_email": "",
                    "category_of_the_email": "Unknown"
                },
                status_code=200
            )

        masked_email, entities = mask_pii(raw_email)

        if masked_email.strip() == "":
            category = "Unknown"
        else:
            try:
                category = model.predict([masked_email])[0]
            except Exception as model_error:
                print(f"Model Prediction Error: {model_error}")
                traceback.print_exc()
                category = "Unknown"

        return {
            "input_email_body": raw_email,
            "list_of_masked_entities": entities,
            "masked_email": masked_email,
            "category_of_the_email": category
        }

    except Exception as e:
        print(f"Error in classify_email: {e}")
        traceback.print_exc()
        return JSONResponse(
            content={
                "input_email_body": req.input_email_body,
                "list_of_masked_entities": [],
                "masked_email": "",
                "category_of_the_email": "Error"
            },
            status_code=500
        )
