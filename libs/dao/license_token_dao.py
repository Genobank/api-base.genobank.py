import datetime
import os

from pymongo import MongoClient

from libs import json_helper_dao


class LicenseTokenDao:
    def __init__(self):
        client = MongoClient(os.getenv("MONGO_DB_HOST"))
        db = client[os.getenv("DB_NAME")]
        self.table = db["license_tokens"]
        self.mongo_db_helper = json_helper_dao.json_helper_dao()

    def fetch(self, _filter={}):
        cur = self.table.find(_filter).sort("createdAt", -1)
        return self.mongo_db_helper.serialize_cur(cur)

    def create(self, data):
        request_biosample = {
            "ip_id": data["ip_id"],
            "license_terms_id": data["license_terms_id"],
            "receiver": data["receiver"],
            "sender": data["sender"],
            "amount": data["amount"],
            "license_token_id": data["license_token_id"],
            "tx_hash": data["tx_hash"],
            "createdAt": datetime.datetime.now(),
            "updatedAt": datetime.datetime.now(),
        }
        inserted = self.table.insert_one(request_biosample)
        return inserted