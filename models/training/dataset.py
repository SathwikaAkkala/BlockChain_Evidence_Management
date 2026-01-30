import pandas as pd
from torch.utils.data import Dataset
from transformers import BertTokenizer


class CrimeDataset(Dataset):

    def __init__(self, file, max_len=128):

        self.data = pd.read_csv(file)
        self.tokenizer = BertTokenizer.from_pretrained(
            "bert-base-uncased"
        )

        self.max_len = max_len

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):

        text = self.data.iloc[idx]["text"]
        label = self.data.iloc[idx]["label"]

        encoding = self.tokenizer(
            text,
            max_length=self.max_len,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )

        return {
            "input_ids": encoding["input_ids"].squeeze(),
            "attention_mask": encoding["attention_mask"].squeeze(),
            "label": label
        }
