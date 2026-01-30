import os
from dotenv import load_dotenv

load_dotenv()

IPFS_URL = os.getenv("IPFS_URL", "/ip4/127.0.0.1/tcp/5001")
TEMP_DIR = "storage/temp"
ENCRYPTED_DIR = "storage/encrypted"
