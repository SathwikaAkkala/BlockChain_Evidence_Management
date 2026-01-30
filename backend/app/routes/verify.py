from fastapi import APIRouter
from pydantic import BaseModel

import torch
from transformers import BertTokenizer

from app.ai.model import load_model


# Router
router = APIRouter()


# Load tokenizer and model once (on server start)
TOKENIZER = BertTokenizer.from_pretrained("bert-base-uncased")

MODEL_PATH = "models/trained/lstm_bert.pt"

model = load_model(MODEL_PATH)


# Request schema
class VerifyRequest(BaseModel):
    text: str


# Response schema
class VerifyResponse(BaseModel):
    risk: str
    confidence: float


@router.post("/verify", response_model=VerifyResponse)
def verify_text(data: VerifyRequest):
    """
    Analyze complaint text using LSTM-BERT
    """

    text = data.text

    # Tokenize
    encoding = TOKENIZER(
        text,
        max_length=128,
        padding="max_length",
        truncation=True,
        return_tensors="pt"
    )

    input_ids = encoding["input_ids"]
    attention_mask = encoding["attention_mask"]

    # Inference
    with torch.no_grad():

        outputs = model(input_ids, attention_mask)

        probs = torch.softmax(outputs, dim=1)

        score, pred = torch.max(probs, dim=1)

        confidence = float(score.item())

        label = int(pred.item())

    # Label mapping
    if label == 1:
        risk = "High Risk (Malicious)"
    else:
        risk = "Low Risk (Normal)"

    return {
        "risk": risk,
        "confidence": round(confidence, 3)
    }
