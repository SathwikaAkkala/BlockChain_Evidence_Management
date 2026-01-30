import torch
from transformers import BertTokenizer

from lstm_bert import LSTMBERT


def predict(text):

    tokenizer = BertTokenizer.from_pretrained(
        "bert-base-uncased"
    )

    model = LSTMBERT()
    model.load_state_dict(
        torch.load("../trained/lstm_bert.pt")
    )

    model.eval()

    encoding = tokenizer(
        text,
        max_length=128,
        padding="max_length",
        truncation=True,
        return_tensors="pt"
    )

    with torch.no_grad():

        output = model(
            encoding["input_ids"],
            encoding["attention_mask"]
        )

        pred = torch.argmax(output, dim=1).item()

    return "Malicious" if pred == 1 else "Normal"


if __name__ == "__main__":

    text = input("Enter complaint: ")

    print("Prediction:", predict(text))
