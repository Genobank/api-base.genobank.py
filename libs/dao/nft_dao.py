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


class NFTDAO:
    def __init__(self):
        self.w3 = Web3(HTTPProvider(os.getenv("CUSTOM_PROVIDER")))
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.account = self.w3.eth.account.privateKeyToAccount(
            os.getenv("BIOSAMPLE_EXECUTOR")
        )
        self.w3.eth.default_account = self.account.address
        # self.SM_JSONINTERFACE_POSP = self.load_smart_contract(os.getenv('ABI_POSP_PATH'))
        self.SM_JSONINTERFACE_POSP_FACTORY = self.load_smart_contract(
            os.getenv("ABI_POSP_FACTORY_PATH")
        )
        self.SM_JSONINTERFACE_POSP = self.load_smart_contract(
            os.getenv("ABI_POSP_PATH")
        )
        self.table = MongoClient(os.getenv("MONGO_DB_HOST"))[os.getenv("DB_NAME")][
            "nfts"
        ]
        # self.db = self.client[os.getenv('DB_NAME')]
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

    def mint(self, contract_address, to_user, to_lab, metadata):
        to_user = web3.Web3.toChecksumAddress(to_user)
        to_lab = web3.Web3.toChecksumAddress(to_lab)
        TokenStruct = [
            0,
            to_user,
            to_lab,
            metadata.get("title", "No foud title"),
            metadata.get("msg", "No founf msg"),
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            metadata.get("name", " no found name"),
            metadata.get("symbol", "no found symbol"),
            contract_address,
        ]

        print("\n\n\n Token struct", TokenStruct)
        tx = self.contract_factory.functions.mintInstancePOSP(
            contract_address, TokenStruct
        ).buildTransaction(
            {"nonce": self.w3.eth.getTransactionCount(self.account.address)}
        )
        signed_tx = self.w3.eth.account.signTransaction(
            tx, private_key=os.getenv("BIOSAMPLE_EXECUTOR")
        )
        tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        self.w3.eth.waitForTransactionReceipt(tx_hash)
        return tx_hash.hex()

    # return {"tx_hash": tx_hash.hex(), "token_id": token_id}

    def get_NFT(self, contract_address, lab_address, user_address):
        contract_address = web3.Web3.toChecksumAddress(contract_address)
        lab_address = web3.Web3.toChecksumAddress(lab_address)
        user_address = web3.Web3.toChecksumAddress(user_address)
        posp_contract = self.w3.eth.contract(
            address=contract_address, abi=self.SM_JSONINTERFACE_POSP["abi"]
        )
        NFT = posp_contract.functions.getPoSP(lab_address, user_address).call(
            {"nonce": self.w3.eth.getTransactionCount(self.account.address)}
        )
        return NFT

    def store_mint_record(self, metadata):
        mint_record = {
            "owner": metadata["owner"],
            "lab_address": metadata["lab_address"],
            "contract_address": metadata["contract_address"],
            "name": metadata["name"],
            "symbol": metadata["symbol"],
            "domain": metadata["domain"],
            "type": metadata["type"],
            "tx_hash": metadata["tx_hash"],
            "token_id": metadata["token_id"],
            "created": datetime.datetime.now(),
            "updated": datetime.datetime.now(),
        }

        inserted = self.table.insert_one(mint_record)
        return inserted

    def fetch(self, _filter={}):
        cur = self.table.find(_filter).sort("createdAt", -1)
        return self.mongo_db_helper.serialize_cur(cur)
