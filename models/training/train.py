import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from transformers import AdamW

from lstm_bert import LSTMBERT
from dataset import CrimeDataset


def train():

    dataset = CrimeDataset("dataset.csv")
    loader = DataLoader(dataset, batch_size=16, shuffle=True)

    model = LSTMBERT()
    optimizer = AdamW(model.parameters(), lr=2e-5)
    loss_fn = nn.CrossEntropyLoss()

    model.train()

    for epoch in range(5):

        total_loss = 0

        for batch in loader:

            optimizer.zero_grad()

            outputs = model(
                batch["input_ids"],
                batch["attention_mask"]
            )

            loss = loss_fn(outputs, batch["label"])
            loss.backward()

            optimizer.step()

            total_loss += loss.item()

        print(f"Epoch {epoch+1} Loss: {total_loss}")

    torch.save(
        model.state_dict(),
        "../trained/lstm_bert.pt"
    )


if __name__ == "__main__":
    train()
