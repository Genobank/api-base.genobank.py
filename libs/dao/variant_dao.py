import datetime
import os

from pymongo import MongoClient

from libs import json_helper_dao


class VariantDAO:
    def __init__(self):
        client = MongoClient(os.getenv("MONGO_DB_HOST"))
        db = client[os.getenv("DB_NAME")]
        self.table = db["variants"]
        self.mongo_db_helper = json_helper_dao.json_helper_dao()

    def fetch(self, _filter={}):
        cur = self.table.find(_filter).sort("createdAt", -1)
        return self.mongo_db_helper.serialize_cur(cur)

    def create(self, variant_data):
        request_biosample = {
            "owner": variant_data["owner"],
            "custodian_address": variant_data["custodian_address"],
            "custodian_serial": variant_data["custodian_serial"],
            "notarizer_address": variant_data["notarizer_address"],
            "notarizer_serial": variant_data["notarizer_serial"],
            "biosampleSerial": variant_data["biosampleSerial"],
            "gene": variant_data["gene"],
            "variant": variant_data["variant"],
            "frequency": variant_data["frequency"],
            "pathogenecity": variant_data["pathogenecity"],
            "disease": variant_data["disease"],
            "ancestry": variant_data["ancestry"],
            "is_clinvar": variant_data["is_clinvar"],
            "tag": variant_data["tag"],
            "externalLink": variant_data["externalLink"],
            "createdAt": datetime.datetime.now(),
            "updatedAt": datetime.datetime.now(),
        }
        inserted = self.table.insert_one(request_biosample)
        return inserted

    def update(self, query_filter, _fields={}):
        if not query_filter:
            raise Exception("Query filter not set")
        query = query_filter
        datetime.datetime.now()
        update = {"$set": _fields}
        result = self.table.update_one(query, update)
        return result.modified_count

    def delete(self, _query={}):
        result = self.table.delete_one(_query)
        return result.deleted_count
