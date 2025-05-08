from pymongo import MongoClient
from libs import mongo_helper_dao
import os
import json
import datetime


class BiosampleFullDao:
	def __init__(self, connection = None):
		client = connection
		if connection is None:
			client = MongoClient(os.getenv('MONGO_DB_HOST'))
		print("\n\n\n client: ", client)
		db = client[os.getenv('DB_NAME')]
		self.table = db["biosample-activations"]
		self.biosample_activations_table = db["biosample-activations"]
		self.biosamples_table = db["biosamples"]
		self.mongo_db_helper = mongo_helper_dao.json_helper_dao()


	def fetch(self, _filters={}):
		biosample_activations = self.biosample_activations_table.find(_filters)
		if not biosample_activations:
			raise ValueError("400 Biosample Activations Not Found")
		else:
			return self.mongo_db_helper.serialize_cur(biosample_activations)
		
	def find_all(self):
		cur = self.table.find().sort('createdAt', -1)
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
		source = {
			"200": "DNA GenoTek",
			"201": "Spectrum"
  	}

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
		return {"data":new_list}