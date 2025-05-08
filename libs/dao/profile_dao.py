import base64
import datetime
import json
import os

import bson
import requests
from pymongo import MongoClient

from libs import json_helper_dao, mongo_helper_dao


class profile_dao:
    def __init__(self):
        client = MongoClient(os.getenv("MONGO_DB_HOST"))
        db = client[os.getenv("DB_NAME")]
        self.table = db.profiles
        self.mongo_db_helper = mongo_helper_dao.json_helper_dao()
        self.json_helper = json_helper_dao.json_helper_dao()
        return None

    def create(self, profile_metadata):
        try:
            profile_metadata["text"] = json.dumps(profile_metadata["text"])
            _json_profile = {
                "serial": profile_metadata["serial"],
                "text": profile_metadata["text"],
                "createdAt": datetime.datetime.now(),
                "updatedAt": datetime.datetime.now(),
            }
            self.table.insert_one(_json_profile)
            return True
        except:
            raise

    def find_all(self):
        try:
            cur = self.table.find().sort("createdAt", -1)
            row = []
            for doc in cur:
                if "_id" in doc:
                    del doc["_id"]
                for key in doc:
                    if (
                        (not isinstance(doc[key], str))
                        and (not isinstance(doc[key], int))
                        and (not isinstance(doc[key], float))
                        and (not isinstance(doc[key], dict))
                    ):
                        doc[key] = str(doc[key])
                try:
                    data = json.loads(doc["text"])
                    if "autograph_signature" in data:
                        del data["autograph_signature"]
                    if "autograph_signature_1" in data:
                        del data["autograph_signature_1"]
                    if "autograph_signature_2" in data:
                        del data["autograph_signature_2"]
                    doc["text"] = str(data)
                except:
                    pass
                row.append(doc)
            return {"data": row}
        except Exception as e:
            print(e)
            return e

    def find_by_serial(self, serial):
        try:
            doc = self.table.find_one({"serial": int(serial)})
            doc = self.mongo_db_helper.serialize_doc(doc)
            data = json.loads(doc["text"])
            if "autograph_signature" in data:
                del data["autograph_signature"]
            if "autograph_signature_1" in data:
                del data["autograph_signature_1"]
            if "autograph_signature_2" in data:
                del data["autograph_signature_2"]
            if "logo" in data:
                try:
                    image = requests.get(data["logo"])
                    image_data = image.content
                    returned_b64 = base64.b64encode(image_data).decode("utf-8")
                    data["logo"] = (
                        f"data:{image.headers['Content-Type'].lower()};base64,{returned_b64}"
                    )
                except requests.exceptions.RequestException:
                    pass
            doc["text"] = json.dumps(data)
            return {"data": doc}
        except Exception as e:
            print(e)
            return False

    def fetch(self, _filter={}, projection={}, exclude=True):
        projection = {field: 0 if exclude else 1 for field in projection}
        cur = self.table.find(_filter, projection).sort("createdAt", -1)
        return self.mongo_db_helper.serialize_cur(cur)

    # def get_name(self, serial):
    # 	query = {
    #         "serial": serial
    #   	}
    # 	doc = self.table.find_one(query)
    # 	return self.json_helper.serialize_doc(doc)
