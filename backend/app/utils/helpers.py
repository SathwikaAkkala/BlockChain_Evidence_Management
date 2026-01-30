import os


def ensure_dirs():

    dirs = [
        "storage/temp",
        "storage/encrypted"
    ]

    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)
