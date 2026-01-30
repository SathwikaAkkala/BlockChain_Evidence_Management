import torch
import torch.nn as nn
from transformers import BertModel


class LSTMBERT(nn.Module):
    """
    Hybrid LSTM + BERT model
    for malicious intent detection
    """

    def __init__(
        self,
        bert_name="bert-base-uncased",
        hidden_size=256,
        num_classes=2
    ):
        super(LSTMBERT, self).__init__()

        # Load pretrained BERT
        self.bert = BertModel.from_pretrained(bert_name)

        # LSTM layer
        self.lstm = nn.LSTM(
            input_size=768,
            hidden_size=hidden_size,
            batch_first=True,
            bidirectional=False
        )

        # Classification layer
        self.fc = nn.Linear(hidden_size, num_classes)

        # Dropout
        self.dropout = nn.Dropout(0.3)

    def forward(self, input_ids, attention_mask):
        """
        Forward pass
        """

        # BERT embeddings
        bert_output = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask
        )

        # Sequence output
        sequence_output = bert_output.last_hidden_state

        # LSTM
        lstm_out, _ = self.lstm(sequence_output)

        # Take last time-step
        last_hidden = lstm_out[:, -1, :]

        # Dropout
        out = self.dropout(last_hidden)

        # Classifier
        logits = self.fc(out)

        return logits


def load_model(model_path=None, device="cpu"):
    """
    Load trained model
    """

    model = LSTMBERT()

    if model_path:
        model.load_state_dict(
            torch.load(model_path, map_location=device)
        )

    model.to(device)
    model.eval()

    return model
