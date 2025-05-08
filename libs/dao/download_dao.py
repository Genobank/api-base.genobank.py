from pymongo import MongoClient
from libs import json_helper_dao
import os
import datetime

class DownloadDAO:
    def __init__(self):
        client = MongoClient(os.getenv('MONGO_DB_HOST'))
        db = client[os.getenv('DB_NAME')]
        self.table = db["downloads"]
        self.mongo_db_helper = json_helper_dao.json_helper_dao()


    def create(self, metadata):
        download_info = {
            "biosample_serial": int(metadata["biosample_serial"]),
            "biosample_owner": metadata["biosample_owner"],
            "downloader_serial": int(metadata["downloader_serial"]),
            "downloader_address": metadata["downloader_address"],
            "custodian_serial": int(metadata["custodian_serial"]),
            "custodian_address": metadata["custodian_address"],
            "tx_hash": metadata["tx_hash"],
            "atp_paid": float(metadata["atp_paid"]),
            "createdAt": datetime.datetime.now(),
            "updatedAt": datetime.datetime.now(),
        }
        inserted = self.table.insert_one(download_info)
        return inserted


    def fetch(self, _filter={}):
        _filter = self.format_download_object(_filter)
        cur = self.table.find(_filter).sort('createdAt', -1)
        return self.mongo_db_helper.serialize_cur(cur)
    

    def count_by_biosample(self, biosample_serial):
        query = {
            "biosample_serial": int(biosample_serial)
        }
        count = self.table.count_documents(query)
        return count
    
    def count_by_biosample_and_downloader(self, biosample_serial, downloader_serial):
        query = {
            "biosample_serial": int(biosample_serial),
            "downloader_serial": int(downloader_serial)
        }
        count = self.table.count_documents(query)
        return count
    
    def count_total_downloads(self):
        return self.table.estimated_document_count()
    

    def format_download_object(self, requester_input):
        if "biosample_serial" in requester_input:
            requester_input["biosample_serial"] = int(requester_input["biosample_serial"])
        if "downloader_serial" in requester_input:
            requester_input["downloader_serial"] = int(requester_input["downloader_serial"])
        if "custodian_serial" in requester_input:
            requester_input["custodian_serial"] = int(requester_input["custodian_serial"])
        if "atp_paid" in requester_input:
            requester_input["atp_paid"] = float(requester_input["atp_paid"])
        return requester_input