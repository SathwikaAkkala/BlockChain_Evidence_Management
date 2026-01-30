"""
AI Model Test Suite
Tests LSTM-BERT loading and inference
"""

import os
import torch

from transformers import BertTokenizer

from backend.app.ai.model import load_model


# Paths
MODEL_PATH = "models/trained/lstm_bert.pt"


def test_model_file_exists():
    """
    Check if trained model file exists
    """
    assert os.path.exists(MODEL_PATH), "Model file not found"


def test_model_load():
    """
    Test model loading
    """
    model = load_model(MODEL_PATH)

    assert model is not None
    assert hasattr(model, "forward")


def test_model_inference():
    """
    Test prediction flow
    """

    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

    model = load_model(MODEL_PATH)

    text = "My bank account was hacked"

    encoding = tokenizer(
        text,
        max_length=128,
        padding="max_length",
        truncation=True,
        return_tensors="pt"
    )

    with torch.no_grad():

        outputs = model(
            encoding["input_ids"],
            encoding["attention_mask"]
        )

        assert outputs is not None
        assert outputs.shape[1] == 2   # Binary classification


def test_multiple_inputs():
    """
    Test batch prediction
    """

    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

    model = load_model(MODEL_PATH)

    texts = [
        "Someone hacked my phone",
        "I forgot my password",
        "Fraud transaction detected"
    ]

    for text in texts:

        encoding = tokenizer(
            text,
            max_length=128,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )

        with torch.no_grad():

            outputs = model(
                encoding["input_ids"],
                encoding["attention_mask"]
            )

            assert outputs.shape == (1, 2)
