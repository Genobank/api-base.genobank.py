import datetime
import json
import os
import re

from pymongo import MongoClient
from web3 import HTTPProvider, Web3
from web3.middleware import geth_poa_middleware

from libs import json_helper_dao, mongo_helper_dao


class delivery_dao:
    def __init__(self):
        self.w3 = Web3(HTTPProvider(os.getenv("CUSTOM_PROVIDER")))
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.executor_pkey = os.getenv("BIOSAMPLE_EXECUTOR")
        self.executor_account = self.w3.eth.account.privateKeyToAccount(
            self.executor_pkey
        )
        self.w3.eth.default_account = self.executor_account.address
        self.SM_JSONINTERFACE = self.load_smart_contract(
            os.getenv("ABI_DELIVER_MANAGER_PATH")
        )
        self.contract_address = os.getenv("DELIVER_MANAGER_CONTRACT")

        client = MongoClient(os.getenv("MONGO_DB_HOST"))
        db = client[os.getenv("DB_NAME")]
        self.table = db["deliveries"]
        self.mongo_db_helper = mongo_helper_dao.json_helper_dao()
        self.json_helper_dao = json_helper_dao.json_helper_dao()

    def load_smart_contract(self, path):
        solcOutput = {}
        try:
            with open(path) as inFile:
                solcOutput = json.load(inFile)
        except Exception as e:
            print(f"ERROR: Could not load file {path}: {e}")
        return solcOutput

    def create(self, delivery_json):
        try:
            json_delibery = {
                "biosample_serial": delivery_json["biosample_serial"],
                "owner": delivery_json["owner"],
                "permittee_id": delivery_json["permittee_serial"],
                "permittee_wallet": delivery_json["user_wallet"],
                "files": delivery_json["file_routes"],
                "type": delivery_json["type"],
                "tx_hash": delivery_json["delivery_tx"],
                "created": datetime.datetime.now(),
                "updated": datetime.datetime.now(),
            }
            inserted = self.table.insert_one(json_delibery)
            return inserted.inserted_id
        except:
            raise

    def find_all(self):
        cur = self.table.find().sort("createdAt", -1)
        return self.json_helper_dao.serialize_cur(cur)

    def find_by_biosample_serial_and_owner(self, biosample_serial, owner):
        doc = self.table.find_one(
            {
                "biosample_serial": int(biosample_serial),
                "owner": re.compile(owner, re.IGNORECASE),
            }
        )
        return self.mongo_db_helper.serialize_doc(doc)

    def find_by_permittee_serial(self, permittee_serial):
        cur = self.table.find({"permittee_id": str(permittee_serial)}).sort(
            "createdAt", -1
        )
        return self.mongo_db_helper.serialize_cur(cur)

    def find_by_biosample_serial(self, biosample_serial):
        cur = self.table.find({"biosample_serial": int(biosample_serial)}).sort(
            "createdAt", -1
        )
        return self.json_helper_dao.serialize_cur(cur)

    def find_by_owner_address(self, owner_address):
        cur = self.table.find({"owner": re.compile(owner_address, re.IGNORECASE)}).sort(
            "createdAt", -1
        )
        return self.json_helper_dao.serialize_cur(cur)

    def notarize(self, serial, owner, lab):
        contract = self.w3.eth.contract(
            address=self.contract_address, abi=self.SM_JSONINTERFACE["abi"]
        )
        tx = contract.functions.delivery(serial, owner, lab).buildTransaction(
            {"nonce": self.w3.eth.getTransactionCount(self.executor_account.address)}
        )
        signed_tx = self.w3.eth.account.signTransaction(
            tx, private_key=self.executor_pkey
        )
        tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        self.w3.eth.waitForTransactionReceipt(tx_hash)
        print("\n\n\n", tx_hash.hex(), "\n\n\n")
        return tx_hash.hex()

    def import_biosamples(self, owner, biosamle_id, file_routes):
        # this function will import the files to the user bucket in a folder names as the biosample_id
        pass

    def cur_to_scheme(self, cur):
        if "_id" in cur:
            del cur["_id"]
        return cur

    def cur_list_to_scheme(self, curlist):
        new_list = []
        for cur in curlist:
            new_list.append(self.cur_to_scheme(cur))
        return {"data": new_list}

    def fetch(self, _filter={}, projection=None, exclude=True, skip=0, limit=0, sort=[("createdAt", -1)], **kwargs):
        if projection:
            projection = {field: 0 if exclude else 1 for field in projection}
        cur = self.table.find(_filter, projection=projection, skip=skip, limit=limit, sort=sort, **kwargs)
        return self.json_helper_dao.serialize_cur(cur)