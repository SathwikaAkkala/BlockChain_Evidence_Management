from web3 import Web3


class Avalanche:

    def __init__(self, rpc):
        self.w3 = Web3(Web3.HTTPProvider(rpc))

    def store(self, cid, hashval):
        print("Blockchain record:", cid, hashval)
