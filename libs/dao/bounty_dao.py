import datetime
import os
from decimal import Decimal

from bson.decimal128 import Decimal128
from pymongo import MongoClient

from libs import json_helper_dao


class BountyDAO:
    def __init__(self):
        client = MongoClient(os.getenv("MONGO_DB_HOST"))
        db = client[os.getenv("DB_NAME")]
        self.table = db["bounty"]
        self.mongo_db_helper = json_helper_dao.json_helper_dao()

    def fetch(self, _filter={}):
        cur = self.table.find(_filter).sort("createdAt", -1)
        return self.mongo_db_helper.serialize_cur(cur)

    def create(self, data):
        request_biosample = {
            "biosample_serial": int(data["biosampleSerial"]),
            "totalamount": float(data["amount"]),  # Mantiene la precisión
            "net_amount": float(data["net_amount"]),  # Mantiene la precisión
            "comission": float(data["comission"]),  # Mantiene la precisión
            "symbol": "ATP",
            "status": "OPEN",
            "status_code": 1,
            "createdAt": datetime.datetime.now(),
            "updatedAt": datetime.datetime.now(),
        }
        inserted = self.table.insert_one(request_biosample)
        return inserted

    def update(self, query_filter, _fields={}):
        if not query_filter:
            raise Exception("Query filter not set")
        query = query_filter
        _fields["updatedAt"] = datetime.datetime.now()
        update = {"$set": _fields}
        result = self.table.update_one(query, update)
        return result.modified_count

    def delete(self, _query={}):
        result = self.table.delete_one(_query)
        return result.deleted_count
