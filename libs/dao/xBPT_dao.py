import json
import os

from web3 import HTTPProvider, Web3
from web3.middleware import geth_poa_middleware


class XBPT_DAO:
    def __init__(self):
        self.w3 = Web3(HTTPProvider(os.getenv("CUSTOM_PROVIDER")))
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.account = self.w3.eth.account.privateKeyToAccount(
            os.getenv("BIOSAMPLE_EXECUTOR")
        )
        self.w3.eth.default_account = self.account.address
        self.XBPT_JSONINTERFACE = self.load_smart_contract(os.getenv("ABI_XBPT_PATH"))
        self.store_contract = self.w3.eth.contract(
            address=os.getenv("xBPT_CONTRACT"), abi=self.XBPT_JSONINTERFACE["abi"]
        )

    def load_smart_contract(self, path):
        solcOutput = {}
        try:
            with open(path) as inFile:
                solcOutput = json.load(inFile)
        except Exception as e:
            print(f"ERROR: Could not load file {path}: {e}")
        return solcOutput

    def notarize_event(self, action_type, metadata):
        tx = self.store_contract.functions.notarize(
            action_type, metadata
        ).buildTransaction(
            {
                "nonce": self.w3.eth.getTransactionCount(
                    self.account.address, "pending"
                ),
            }
        )
        gas_estimate = self.w3.eth.estimateGas(tx)
        tx["gas"] = gas_estimate
        signed_tx = self.w3.eth.account.signTransaction(
            tx, private_key=os.getenv("BIOSAMPLE_EXECUTOR")
        )
        tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        self.w3.eth.waitForTransactionReceipt(tx_hash)
        return tx_hash.hex()

    def get_event_by_index(self, _index):
        avax_price = self.store_contract.functions.getEvent(_index).call(
            {"nonce": self.w3.eth.getEvent(self.account.address)}
        )
        return avax_price

    def get_all_events(self):
        avax_price = self.store_contract.functions.getEvent().call(
            {"nonce": self.w3.eth.getAllEvents(self.account.address)}
        )
        return avax_price

    def get_event_count(self):
        avax_price = self.store_contract.functions.getEvent().call(
            {"nonce": self.w3.eth.getEventCount(self.account.address)}
        )
        return avax_price
