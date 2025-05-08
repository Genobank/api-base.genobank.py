import datetime
import os

from pymongo import MongoClient

from libs import json_helper_dao


class BiosampleTransferHistoryDAO:
    def __init__(self):
        client = MongoClient(os.getenv("MONGO_DB_HOST"))
        db = client[os.getenv("DB_NAME")]
        self.table = db["biosample-transfer-history"]
        self.mongo_db_helper = json_helper_dao.json_helper_dao()

    def fetch(self, _filter={}, projection=None, exclude=True, skip=0, limit=0, sort=[("createdAt", -1)], **kwargs):
        if projection:
            projection = {field: 0 if exclude else 1 for field in projection}
        cur = self.table.find(_filter, projection=projection, skip=skip, limit=limit, sort=sort, **kwargs)
        return self.mongo_db_helper.serialize_cur(cur)

    def create(self, data):
        request_biosample = {
            "biosample_serial": int(data["biosample_serial"]),
            "from": data["from"],
            "to": data["to"],
            "MTA": data["MTA"],
            "mta_custidian_signature": data["mta_custidian_signature"],
            "mta_executor_signature": data["mta_executor_signature"],
            "mta_receiver_signature": data.get("mta_receiver_signature", ""),
            "tx_hash": data.get("tx_hash", ""),
            "status": "PENDING",
            "status_code": 0,
            "createdAt": datetime.datetime.now(),
            "updatedAt": datetime.datetime.now(),
        }
        inserted = self.table.insert_one(request_biosample)
        return inserted

    def update(self, query_filter, _fields={}):
        if not query_filter:
            raise ValueError("Query filter not set")
        if not _fields:
            raise ValueError("Fields to update not set")
        query = query_filter
        _fields["updatedAt"] = datetime.datetime.now()
        update = {"$set": _fields}
        result = self.table.update_one(query, update)
        return result.modified_count

    def delete(self, _query={}):
        result = self.table.delete_one(_query)
        return result.deleted_count
