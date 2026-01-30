"""
Storage Module Test Suite
Tests storage directories and files
"""

import os
import json
import tempfile
import shutil


# Base storage path
STORAGE_DIR = "storage"


def test_storage_root_exists():
    """
    Check storage folder exists
    """
    assert os.path.exists(STORAGE_DIR)


def test_required_folders_exist():
    """
    Check all main subfolders exist
    """

    folders = [
        "encrypted",
        "decrypted",
        "temp",
        "logs",
        "backups"
    ]

    for folder in folders:
        path = os.path.join(STORAGE_DIR, folder)
        assert os.path.isdir(path), f"{folder} folder missing"


def test_log_files_exist():
    """
    Check log files exist
    """

    logs = [
        "audit.log",
        "custody.log",
        "access.log"
    ]

    for log in logs:
        path = os.path.join(STORAGE_DIR, "logs", log)
        assert os.path.isfile(path), f"{log} missing"


def test_metadata_files_exist():
    """
    Check metadata and index files
    """

    files = [
        "metadata.json",
        "index.json",
        "README.txt"
    ]

    for file in files:
        path = os.path.join(STORAGE_DIR, file)
        assert os.path.isfile(path), f"{file} missing"


def test_temp_file_creation_and_cleanup():
    """
    Test temp file write and delete
    """

    temp_dir = os.path.join(STORAGE_DIR, "temp")

    # Create temp file
    fd, path = tempfile.mkstemp(dir=temp_dir)

    with os.fdopen(fd, "wb") as f:
        f.write(b"Temporary evidence")

    # Check file created
    assert os.path.exists(path)

    # Delete file
    os.remove(path)

    assert not os.path.exists(path)


def test_encrypted_storage_write():
    """
    Test writing encrypted file
    """

    enc_dir = os.path.join(STORAGE_DIR, "encrypted")

    file_path = os.path.join(enc_dir, "test.enc")

    with open(file_path, "wb") as f:
        f.write(b"EncryptedData123")

    assert os.path.exists(file_path)

    # Cleanup
    os.remove(file_path)


def test_backup_creation():
    """
    Test backup file creation
    """

    backup_dir = os.path.join(STORAGE_DIR, "backups")

    file_path = os.path.join(backup_dir, "backup_test.bak")

    with open(file_path, "w") as f:
        f.write("Backup content")

    assert os.path.exists(file_path)

    # Cleanup
    os.remove(file_path)


def test_index_json_format():
    """
    Validate index.json structure
    """

    index_path = os.path.join(STORAGE_DIR, "index.json")

    with open(index_path, "r") as f:
        data = json.load(f)

    assert isinstance(data, dict)
    assert "records" in data or "evidence_records" in data
