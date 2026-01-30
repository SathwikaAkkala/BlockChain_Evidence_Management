import ipfshttpclient
from app.config import IPFS_URL


client = ipfshttpclient.connect(IPFS_URL)


def upload(path):

    res = client.add(path)

    return res["Hash"]
