import json
import os

DB_FILE = "storage/index.json"


def save_record(data):

    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump([], f)

    with open(DB_FILE, "r+") as f:

        records = json.load(f)
        records.append(data)

        f.seek(0)
        json.dump(records, f, indent=2)
