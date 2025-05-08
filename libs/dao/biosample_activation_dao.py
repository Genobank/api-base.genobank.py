import datetime
import json
import os

from pymongo import MongoClient

from libs import mongo_helper_dao


class biosample_activation_dao:
    def __init__(self):
        client = MongoClient(os.getenv("MONGO_DB_HOST"))
        db = client[os.getenv("DB_NAME")]
        self.table = db["biosample-activations"]
        self.mongo_db_helper = mongo_helper_dao.json_helper_dao()

    def fetch(self, _filter={}, projection={}):
        cur = self.table.find(_filter, projection).sort("createdAt", -1)
        return self.mongo_db_helper.serialize_cur(cur)

    def create_in_db(self, data):
        biosample_activation_data = {
            "serial": int(data["biosampleId"]),
            "permitteeSerial": str(data["permittee_id"]),
            "physicalId": str(data["physicalId"]),
            "createdAt": datetime.datetime.now(),
            "updatedAt": datetime.datetime.now(),
        }

        inserted = self.table.insert_one(biosample_activation_data)
        return inserted

    def find_all(self):
        cur = self.table.find().sort("createdAt", -1)
        return self.mongo_db_helper.serialize_cur(cur)

    def find_by_serial(self, serial):
        serial = int(serial)
        doc = self.table.find_one({"serial": serial})
        return self.mongo_db_helper.serialize_doc(doc)

    def find_all_filtered(self, filter):
        custom_filter = filter
        if not isinstance(custom_filter, dict):
            raise ValueError("Filter must be a dictionary")
        if "serial" in custom_filter:
            custom_filter["serial"] = int(custom_filter["serial"])

        print("\n\n custom_filter", custom_filter)
        cur = self.table.find(custom_filter)
        return self.mongo_db_helper.serialize_cur(cur)

    def cur_to_scheme(self, cur):
        source = {"200": "DNA GenoTek", "201": "Spectrum"}

        if "_id" in cur:
            del cur["_id"]
        if "physicalId" in cur:
            prefix = cur["physicalId"][0:3]
            manufacturer = "Not registered"
            if prefix in source:
                manufacturer = source[prefix]
            cur["manufacturer"] = manufacturer
        return cur

    def cur_list_to_scheme(self, curlist):
        new_list = []
        for cur in curlist:
            new_list.append(self.cur_to_scheme(cur))
        return {"data": new_list}


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
