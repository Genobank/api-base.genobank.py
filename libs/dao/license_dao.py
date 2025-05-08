from dotenv import load_dotenv
from pymongo import MongoClient
import json
import os, os.path
import datetime

class license_dao:
	def __init__(self):
		self.client = MongoClient(os.getenv('MONGO_DB_HOST'))
		self.db = self.client[os.getenv('DB_NAME')]
		self.table = self.db.licenses
		
	def create_licence (self, licence_metadata):
		try:
			licence_metadata = json.loads(licence_metadata)
			licence_details = self.get_licence_details(int(licence_metadata["type"]))
			exist_licence = self.find_license_by_permitee_and_type(licence_metadata["owner"], licence_metadata["type"])
			print(exist_licence)
			if exist_licence:
				raise Exception('Could not create license, because it already exists')
			_fields = {
				"license_owner": str(licence_metadata["owner"]).upper(),
				"license_type": licence_metadata["type"],
				"license_name": licence_details["license_name"],
				"code": licence_details["code"],
				"created": str(datetime.datetime.now()),
				"updated": str(datetime.datetime.now()),
				"expiration": str(datetime.datetime.fromtimestamp(licence_metadata["expiration"]))
			}
			self.table.insert_one(_fields)
			return True
		except:
			raise

	def delete_license (self, permittee, type):
		pmttee = str(permittee).upper()
		query = {"license_owner": pmttee, "license_type": int(type)}
		self.table.delete_one(query)
		return True

	def get_licence_details(self, type):
		try:
			_licences = [
				{},
				{"license_name": "ANCESTRY", "code": "ACTRY"},
				{"license_name": "PROOF OF STAKE PROTOCOL", "code": "POSP"},
			]
			if type == 0 or type >= len(_licences):
				raise Exception("Error: Type of licence not valid 'license_type' must be diferet to '0' and less than '"+str(len(_licences))+"'")
			return _licences[type]
		except Exception as e:
			raise e

	def find_license_by_type(self, type):
		try:
			cur = self.table.find({"license_type": int(type)})
			row = []
			for doc in cur:
				for key in doc:
					if (not isinstance(doc[key], str)) or (not isinstance(doc[key], int)) or (not isinstance(doc[key], float)):
						doc[key] = str(doc[key])
				row.append(doc)
			return row
		except Exception as e:
			print(e)
			return False

	def find_license_by_permitee(self, permittee):
		try:
			cur = self.table.find({"license_owner": permittee})
			row = []
			for doc in cur:
				for key in doc:
					if (not isinstance(doc[key], str)) or (not isinstance(doc[key], int)) or (not isinstance(doc[key], float)):
						doc[key] = str(doc[key])
				row.append(doc)
			return row
		except Exception as e:
			print(e)
			return False

	def find_license_by_permitee_and_type(self, permittee, type):
		try:
			cur = self.table.find({"license_owner": str(permittee).upper(), "license_type": int(type)})
			row = []
			for doc in cur:
				for key in doc:
					if (not isinstance(doc[key], str)) or (not isinstance(doc[key], int)) or (not isinstance(doc[key], float)):
						doc[key] = str(doc[key])
				row.append(doc)
			return row
		except Exception as e:
			print(e)
			return False