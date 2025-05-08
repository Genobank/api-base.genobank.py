
from pymongo import MongoClient
import os
import json
import datetime
import re
from libs import mongo_helper_dao
from libs import json_helper_dao
from libs.dao import profile_dao



class shared_dao:
	def __init__(self):
		self.client = MongoClient(os.getenv('MONGO_DB_HOST'))
		self.db = self.client[os.getenv('DB_NAME')]
		self.table = self.db.shares
		self.table_profiles = self.db.profiles
		self.mongo_db_helper = mongo_helper_dao.json_helper_dao()
		self.json_helper_dao = json_helper_dao.json_helper_dao()
		self.profile_dao = profile_dao.profile_dao()


		return None

	def find_shares_by_user(self, user, file_hash):

		print("user", user)
		print("file_hash", file_hash)
		cur = self.table.find({"user":user, "filehash":file_hash})

		return self.mongo_db_helper.serialize_cur(cur)
	
	def find_shares_by_filehash(self, user, filehash):
		cur = self.table.find({"filehash": filehash})
		return self.mongo_db_helper.serialize_cur(cur)


	def get_enabled_list(self, pmttee_lst, shares_list):
		share_serials = {share["serial"] for share in shares_list}
		enabled_permittees = [permittee for permittee in pmttee_lst if int(permittee["serial"]) not in share_serials]
		return enabled_permittees
	
	def find_shares_by_hash_and_permittee(self, file_hash, permittee):
		cur = self.table.find_one({"hash":file_hash, "permittee":permittee})
		return cur
	
	def share_file(self, data):
		exist = self.find_shares_by_hash_and_permittee(data["fileHash"], data["permittee"])
		print("USER:", data["user"])
		print("PERMIT:", data["permittee"])

		print(exist)
		if exist:
			raise Exception("This file is already shared with this permittee")
		_fields = {
			"user": data["user"],
			"filename": data["filename"],
			"permittee": str(data["permittee"]),
			"serial": data["serial"],
			"agreements": data["agreements"],
			"agreements_signature": data["signature"],
			"filehash": data["fileHash"],
			"transaction_hash": data["tx_hash"],
			"revoked": False,
			"created": datetime.datetime.now(),
			"updated": datetime.datetime.now()
		}
		print("\n\n",_fields,"\n\n")
		inserted = self.table.insert_one(_fields)
		return {"iserted":inserted.inserted_id}

	def find_shared_files_by_lab (self, lab):
		try:
			cur = self.table.find({"permittee": re.compile(lab, re.IGNORECASE)})
			return self.json_helper_dao.serialize_cur(cur)
			# rows = []
			# for doc in cur:
			# 	for key in doc:
			# 		if (not isinstance(doc[key], str)) and (not isinstance(doc[key], int)) and (not isinstance(doc[key], float) and (not isinstance(doc[key], dict)) ):
			# 			doc[key] = str(doc[key])
			# 	rows.append(doc)
			# return rows
		except Exception as e:
			print(e)
			return False

	def get_enabled_profiles_from_lab_list(self, enable_lab_list):
		# all_profiles = self.find_all_profiles()
		all_profiles = self.profile_dao.find_all()["data"]
		matching_profiles = []
		for p in all_profiles:
			for pe in enable_lab_list:
				if int(p['serial']) == int(pe['serial']):
					p['owner'] = pe['owner']  # Agregar el campo "owner"
					matching_profiles.append(p)
					break  # Salir del ciclo interno una vez que encontramos un match
		return {"data": matching_profiles}




	def is_revoked(self, filename, permittee):
		try:
			cur = self.table.find_one({"filename": filename, "permittee": re.compile(permittee, re.IGNORECASE)})
			revoked = cur["revoked"]
			return (str(revoked).lower() == "true")
		except Exception as e:
			print("Error:",e)
			return e

	def revoke_consents(self, user, permittee):
		try:
			self.table.update_one({
				"user":re.compile(user, re.IGNORECASE),
				"permittee":re.compile(permittee, re.IGNORECASE)
				}, 
				{"$set":
					{"revoked": True}
				}
			)
			return {"revoked":"File revoked successfully"}
		except Exception as e:
			print(e)
			return False
		
	def fetch(self, _filter={}):
		cur = self.table.find(_filter).sort('createdAt', -1)
		return self.json_helper_dao.serialize_cur(cur)