import os
import uuid

from fastapi import APIRouter, UploadFile, File

from app.crypto.aes import encrypt_data
from app.crypto.hash import sha256
from app.ipfs.ipfs_client import upload
from app.config import TEMP_DIR, ENCRYPTED_DIR
from app.database import save_record


router = APIRouter()


@router.post("/submit")
async def submit(file: UploadFile = File(...)):

    data = await file.read()

    file_id = str(uuid.uuid4())

    temp_path = f"{TEMP_DIR}/{file_id}.tmp"
    enc_path = f"{ENCRYPTED_DIR}/{file_id}.bin"

    # Save temp
    with open(temp_path, "wb") as f:
        f.write(data)

    # Encrypt
    key = b"0" * 32
    nonce, cipher = encrypt_data(data, key)

    with open(enc_path, "wb") as f:
        f.write(cipher)

    # Upload to IPFS
    cid = upload(enc_path)

    # Hash
    file_hash = sha256(cipher)

    # Save DB
    save_record({
        "id": file_id,
        "cid": cid,
        "hash": file_hash
    })

    return {
        "id": file_id,
        "cid": cid,
        "hash": file_hash,
        "status": "success"
    }
