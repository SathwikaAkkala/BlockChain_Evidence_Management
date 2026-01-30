import os
import json
import time
import hashlib

from fastapi import APIRouter
from pydantic import BaseModel


# Router
router = APIRouter()


# Log file
CUSTODY_FILE = "storage/logs/custody.log"


# Request schema
class CustodyRequest(BaseModel):
    evidence_id: str
    actor: str
    action: str


# Response schema
class CustodyResponse(BaseModel):
    status: str
    record_hash: str


def ensure_file():

    if not os.path.exists("storage/logs"):
        os.makedirs("storage/logs")

    if not os.path.exists(CUSTODY_FILE):
        with open(CUSTODY_FILE, "w") as f:
            f.write("")


def log_action(evidence_id, actor, action):

    ensure_file()

    timestamp = int(time.time())

    record = {
        "evidence_id": evidence_id,
        "actor": actor,
        "action": action,
        "timestamp": timestamp
    }

    record_str = json.dumps(record, sort_keys=True)

    record_hash = hashlib.sha256(
        record_str.encode()
    ).hexdigest()

    log_entry = {
        "record": record,
        "hash": record_hash
    }

    with open(CUSTODY_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    return record_hash


@router.post("/custody", response_model=CustodyResponse)
def add_custody(data: CustodyRequest):
    """
    Add custody record
    """

    record_hash = log_action(
        data.evidence_id,
        data.actor,
        data.action
    )

    return {
        "status": "logged",
        "record_hash": record_hash
    }


@router.get("/custody/{evidence_id}")
def get_custody(evidence_id: str):
    """
    Get custody history of evidence
    """

    ensure_file()

    history = []

    with open(CUSTODY_FILE, "r") as f:

        for line in f:

            if not line.strip():
                continue

            entry = json.loads(line)

            if entry["record"]["evidence_id"] == evidence_id:
                history.append(entry)

    return {
        "evidence_id": evidence_id,
        "history": history
    }
