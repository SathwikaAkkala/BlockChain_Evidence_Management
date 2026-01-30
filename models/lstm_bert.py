import torch
import torch.nn as nn
from transformers import BertModel


class LSTMBERT(nn.Module):

    def __init__(self):
        super(LSTMBERT, self).__init__()

        self.bert = BertModel.from_pretrained("bert-base-uncased")
        self.lstm = nn.LSTM(
            input_size=768,
            hidden_size=256,
            batch_first=True
        )

        self.fc = nn.Linear(256, 2)

    def forward(self, input_ids, attention_mask):

        bert_out = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask
        )

        lstm_out, _ = self.lstm(bert_out.last_hidden_state)

        output = self.fc(lstm_out[:, -1, :])

        return output
