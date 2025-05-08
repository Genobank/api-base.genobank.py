from pymongo import MongoClient
from libs import json_helper_dao
import os
import datetime

class AppJwtDAO:
    def __init__(self):
        client = MongoClient(os.getenv('MONGO_DB_HOST'))
        db = client[os.getenv('DB_NAME')]
        self.table = db["app_jwt"]
        self.mongo_db_helper = json_helper_dao.json_helper_dao()

    def fetch(self, _filter={}):
        cur = self.table.find(_filter).sort('createdAt', -1)
        return self.mongo_db_helper.serialize_cur(cur)
        
    def create(self, sales_metadata):
      request_biosample = {
         "jwt": sales_metadata["jwt"],
         "domain": sales_metadata["domain"],
         "env": sales_metadata["env"],
         "expiration": sales_metadata["expiration"],
         "createdAt": datetime.datetime.now(),
         "updatedAt": datetime.datetime.now(),
      }
      inserted = self.table.insert_one(request_biosample)
      return inserted