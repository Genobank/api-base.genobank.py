from pymongo import MongoClient
import os
import re
import datetime


class pending_permittee_dao:
	def __init__(self):
		self.client = MongoClient(os.getenv('MONGO_DB_HOST'))
		self.db = self.client[os.getenv('DB_NAME')]
		self.table = self.db["pending-permittees"]
		self.permittee_table = self.db.permittees
		return None


# Status codes (0: pending, 1: Aprobed, 2: Rejected)
	def create(self, all_data):
		_pendig_permittee = {
			"owner": all_data["Owner"],
			"status":0,
			"text":{
				"name": all_data["LaboratoryName"],
				"investigator": all_data["PrincipalInvestigator"],
				"title": all_data["Title"],
				"titleCode": all_data["TitleCode"],
				"logo": all_data["UrlLabLogo"],
				"labType":all_data["Labtype"],
				"labTypeCode":all_data["LabTypeCode"],
				"firstAddress":all_data["FirstAddress"],
				"secondAddress":all_data["SecondAddress"],
				"country":all_data["Country"],
				"countryCode":all_data["CountryCode"],
				"webpage":all_data["Webpage"],
				"email":all_data["Email"],
				"licenseNumber":all_data["LicenseNumber"],
				"twitter":all_data["Twitter"],
				"linkedin":all_data["Linkedin"],
				"phone":all_data["Phone"],
				"clia":all_data["Clia"]
			},
			"createdAt":datetime.datetime.now(),
			"updatedAt":datetime.datetime.now()
		}
		print(_pendig_permittee)

		inserted = self.table.insert_one(_pendig_permittee)
		print(type(inserted.inserted_id))
		print(inserted.inserted_id)
		return {"insertedID": str(inserted.inserted_id)}
	
	def find_all_pendig_permittees(self):
		try:
			cur = self.table.find()
			rows = []
			for doc in cur:
				for key in doc:
					if (not isinstance(doc[key], str)) and (not isinstance(doc[key], int)) and (not isinstance(doc[key], float) and (not isinstance(doc[key], dict)) ):
						doc[key] = str(doc[key])
				rows.append(doc)
			return rows
		except Exception as e:
			print(e)
			return False
		
		
	def change_pending_permittee_status(self, owner, status):
		try:
			query = {"owner": {"$regex": f"^{owner}$", "$options": "i"}}
			update = {"$set": {"status": status}}
			self.table.update_one(query, update)
		except Exception as e:
			print(e)
			return e
		
	def add_pendig_serial(self, owner, serial):
		query = {"owner": {"$regex": f"^{owner}$"}}
		update = {"$set": {"serial": serial}}
		self.table.update_one(query, update)
		return True




		

	def find_by_owner(self, owner):
		try:
			cur = self.table.find_one({"owner": re.compile(owner, re.IGNORECASE)})
			return cur
		except Exception as e:
			print(e)
			return e
		

	def approve_permittee(self, elements):
		existing_serials = set(self.permittee_table.distinct("serial"))
		existing_serials = sorted(existing_serials)
		next_serial = 1
		while next_serial in existing_serials:
			next_serial += 1
		return {"fields":existing_serials}



