import datetime
import hashlib
import hmac
import json
import os
import re

import requests
from pymongo import MongoClient

from libs import json_helper_dao, mongo_helper_dao


class magic_link_dao:
    def __init__(self):
        client = MongoClient(os.getenv("MONGO_DB_HOST"))
        db = client[os.getenv("DB_NAME")]
        self.table = db["magic_link"]
        self.table_biosample_activations = db["magic_link"]
        self.mongo_db_helper = mongo_helper_dao.json_helper_dao()
        self.json_db_helper = json_helper_dao.json_helper_dao()

    def save_db(self, metadata, url):
        magic_link = {
            "creator": metadata["permittee"],
            "creator_id": metadata["permittee_id"],
            "link": url,
            "prefix": metadata["prefix"],
            "packageHashCode": metadata["packageHashCode"],
            "biosample_id": int(metadata["biosampleId"]),
            "createdAt": datetime.datetime.now(),
            "updatedAt": datetime.datetime.now(),
        }

        inserted = self.table.insert_one(magic_link)
        return inserted

    def create_biosample_activation(self, biosample_id, permittee_id, physical_id):
        try:
            _hmac = self.create_biosample_hmac(biosample_id, os.getenv("APP_SECRET"))
            url = os.getenv("API_BASE") + "/biosample-activation"
            headers = {"Content-Type": "application/json"}
            body = json.dumps(
                {
                    "serial": biosample_id,
                    "biosampleSecret": _hmac,
                    "physicalId": physical_id,
                    "permitteeSerial": permittee_id,
                }
            )

            response = requests.post(url, headers=headers, data=body)
            response.raise_for_status()  # Esto generará un error si la respuesta HTTP tiene un código de estado 4xx o 5xx
            return response.json()
        except requests.RequestException as error:
            print(f"Error: {error}")
            return {"error": str(error)}

    def fetch(self, _filter={}):
        if "creator_id" in _filter:
            _filter["creator_id"] = int(_filter["creator_id"])
        if "biosample_id" in _filter:
            _filter["biosample_id"] = int(_filter["biosample_id"])
        cur = self.table.find(_filter).sort("createdAt", -1)
        return self.json_db_helper.serialize_cur(cur)

    def delete(self, _query={}):
        result = self.table.delete_one(_query)
        return result.deleted_count

    # def create_biosample_hmac(self, biosample_id, app_secret):
    #   # Convert strings to bytes
    #   biosample_id_bytes = biosample_id.encode('utf-8')
    #   app_secret_bytes = app_secret.encode('utf-8')

    #   # Create HMAC using SHA-256
    #   signature = hmac.new(app_secret_bytes, biosample_id_bytes, digestmod=hashlib.sha256).hexdigest()

    #   # Convert HMAC signature to hex format
    #   return signature

    def create_biosample_hmac(self, biosample_id):
        hmac1 = hmac.new(
            os.getenv("BIOSAMPLE_ACTIVATION_SECRET").encode("utf-8"),
            msg=str(biosample_id).encode(),
            digestmod="sha256",
        )
        signature = str(hmac1.hexdigest())

        return signature

    def create_activation_url(
        self, url_base, biosample_id, permittee_id, physical_id, activation_secret
    ):
        return f"{url_base}/?biosampleId={biosample_id}&laboratoryId={permittee_id}&physicalId={physical_id}#{activation_secret}"

    def find_all(self):
        cur = self.table.find()
        return self.mongo_db_helper.serialize_cur(cur)

    def find_by_creator_wallet(self, wallet):
        cur = self.table.find({"creator": re.compile(wallet, re.IGNORECASE)})
        return self.mongo_db_helper.serialize_cur(cur)

    def find_by_creator_serial(self, serial):
        cur = self.table.find({"creator_id": serial})
        return self.json_db_helper.serialize_cur(cur)

    def is_link_creator(self, creator_wallet, link):
        query = {"creator": re.compile(creator_wallet, re.IGNORECASE), "link": link}
        doc = self.table.find_one(query)
        magic_link = self.json_db_helper.serialize_doc(doc)
        if magic_link:
            return True
        return False
