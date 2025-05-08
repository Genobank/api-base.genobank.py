# from datetime import datetime
import datetime
import json
import os
import os.path
import re

import requests
import web3
from dotenv import load_dotenv
from pymongo import MongoClient
from web3 import HTTPProvider, Web3
from web3.auto import w3
from web3.middleware import geth_poa_middleware

from libs import json_helper_dao


class ContractDAO:
    def __init__(self):
        self.w3 = Web3(HTTPProvider(os.getenv("CUSTOM_PROVIDER")))
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.account = self.w3.eth.account.privateKeyToAccount(
            os.getenv("BIOSAMPLE_EXECUTOR")
        )
        self.w3.eth.default_account = self.account.address
        self.SM_JSONINTERFACE_POSP_FACTORY = self.load_smart_contract(
            os.getenv("ABI_POSP_FACTORY_PATH")
        )
        self.table = MongoClient(os.getenv("MONGO_DB_HOST"))[os.getenv("DB_NAME")][
            "contracts"
        ]
        self.contract_factory = self.w3.eth.contract(
            address=os.getenv("POSP_FACTORY_CONTRACT"),
            abi=self.SM_JSONINTERFACE_POSP_FACTORY["abi"],
        )
        self.mongo_db_helper = json_helper_dao.json_helper_dao()

    def load_smart_contract(self, path):
        solcOutput = {}
        try:
            with open(path) as inFile:
                solcOutput = json.load(inFile)
        except Exception as e:
            print(f"ERROR: Could not load file {path}: {e}")
        return solcOutput

    def deploy(self, name, symbol, lab_address):
        if len(symbol) > 11:
            raise Exception("Error the symbol must not contain more than 11 characters")
        lab_address_checksum = web3.Web3.toChecksumAddress(lab_address)
        transaction = self.contract_factory.functions.createToken(
            name, symbol, lab_address_checksum
        ).buildTransaction(
            {"nonce": self.w3.eth.getTransactionCount(self.account.address)}
        )
        signed_tx = self.w3.eth.account.signTransaction(
            transaction, private_key=os.getenv("BIOSAMPLE_EXECUTOR")
        )
        tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        logs = self.contract_factory.events.tokenCreationEvent().processReceipt(receipt)
        if logs:
            event = logs[0]
            contract_address = event["args"]["sm_address"]
        print("tx_hash: ", tx_hash.hex())
        print("contract_address: ", contract_address)

        return {"tx_hash": tx_hash.hex(), "deployed_smartcontract": contract_address}

    def store_deployment_record(self, metadata):
        deployment_record = {
            "address": metadata["address"],
            "owner": metadata["owner"],
            "lab_address": metadata["lab_address"],
            "name": metadata["name"],
            "tx_hash": metadata["tx_hash"],
            "domain": metadata["domain"],
            "symbol": metadata["symbol"],
            "type": metadata["type"],
            "created": datetime.datetime.now(),
            "updated": datetime.datetime.now(),
        }

        inserted = self.table.insert_one(deployment_record)
        return inserted

    def fetch(self, _filter={}):
        cur = self.table.find(_filter).sort("createdAt", -1)
        return self.mongo_db_helper.serialize_cur(cur)
