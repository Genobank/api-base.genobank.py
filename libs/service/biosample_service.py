import hmac
import os
from typing import List

from libs.dao import biosample_dao
from libs.exceptions import DomainInjectionError


class biosample_service:
	def __init__(self, _biosample,):
		if not isinstance(_biosample, biosample_dao.biosample_dao):
			raise DomainInjectionError.DomainInjectionError("genotype_service", "genotype")		
		self.biosample = _biosample


	def find_all(self):
		biosamples = self.biosample.find_all()
		# biosamples = biosamples[0] if len(biosamples) == 1 else biosamples
		if not biosamples:
			return []
		else:
			return self.biosample.cur_list_to_scheme(biosamples)

		
	def find_all_by_serials(self, serials):
		serials_int = [int(serial) for serial in serials]
		biosamples = self.biosample.fetch({"serial": {"$in": serials_int}})
		if not biosamples:
			return []
		else:
			return self.biosample.cur_list_to_scheme(biosamples)


	def fetch(self, _filters={}, _projection={}):
		biosamples = self.biosample.fetch(_filters, _projection)
		return self.biosample.cur_list_to_scheme(biosamples)
		

	def fetch_one(self, _filters={}):
		biosamples = self.biosample.fetch(_filters)
		if not biosamples:
			return []
		return biosamples[0]
		
	def find_all_by_permittee_serial(self, serial):
		biosample_list = self.biosample.find_all_by_permittee_serial(serial)
		if not biosample_list:
			return []
		else:
			return self.biosample.cur_list_to_scheme(biosample_list)
		
	def filter_biosamples_by_activation(self, biosamples, biosample_activations):
		activation_serials = set([activation['serial'] for activation in biosample_activations])
		filtered_biosamples = [biosample for biosample in biosamples if biosample['serial'] in activation_serials]
		return {"data":filtered_biosamples}
	

	def fetch_biosamples_by_full_fields(self, biosamples, biosample_activations):
		biosamples_dict = {sample['serial']: sample for sample in biosamples}
		for activation in biosample_activations:
				serial = activation['serial']
				if serial in biosamples_dict:
						combined_dict = {**activation, **biosamples_dict[serial]}
						deliveries = self.biosample.find_files_by_biosample_serial(serial)
						files_count = 0
						if deliveries:
							file_paths = [
								value for delivery in deliveries 
								for value in (delivery["files"].values() if isinstance(delivery["files"], dict) else delivery["files"])
							]
							files_count = len(file_paths)
						combined_dict["files_count"] = files_count
						biosample_history = self.biosample.fetch_bisample_transfer_history(_filter={"biosample_serial": int(serial), "status": "PENDING"})
						combined_dict["transferable"] = len(biosample_history) == 0 and files_count == 0
						biosamples_dict[serial] = combined_dict
		combined_list = list(biosamples_dict.values())
		return combined_list
	

	def filter_biosamples(self, full_biosamples, _filter):
		biosamples = []
		for biosample in full_biosamples:
			for key in _filter:
				if key in biosample and biosample[key] == _filter[key]:
					biosamples.append(biosample)
		return biosamples
	

	def fetch_biosamples_by_dynamic_filter(self, _filter):
		biosamples = self.biosample.fetch_biosamples_by_dynamic_filter(_filter)
		if not biosamples:
			raise ValueError("400 Biosample Not Found")
		else:
			return self.biosample.cur_list_to_scheme(biosamples)

			
	def claim(self, token_id, data):
		if not token_id:
			raise Exception("Invalid token_id")
		return self.biosample.claim(token_id, data)
	
	def find_biosample_by_serial(self, serial):
		biosample = self.biosample.find_biosample_by_serial(serial)
		return biosample
	
	def find_biosample_details_by_serial(self, serial):
		biosample = self.biosample.find_biosample_details_by_serial(serial)
		if not biosample:
			return []
		return biosample[0]
	
	def find_serializable_biosample_by_serial(self, serial):
		biosample = self.biosample.find_serializable_biosample_by_serial(serial)
		return biosample
	
	def find_biosample_by_serial_or_die(self, serial):
		biosample = self.biosample.find_biosample_by_serial(serial)
		if not biosample:
			raise Exception("Invalid biosample")
		return biosample
	
	def verify_biosample_ownership(self, biofile_object, owner):
		return str(biofile_object["owner"]).upper() == str(owner).upper() 

	def verify_biosample_ownership_or_die(self, biosample_object, owner):
		is_owner = str(biosample_object["owner"]).upper() == str(owner).upper()
		if not is_owner:
			raise ValueError("Wrong ownership for biosample")
		
	def is_owner_or_die(self, serial, owner):
		is_owner = self.biosample.find_by_serial_and_owner(serial, owner)
		if not is_owner:
			raise Exception("This user is not allowed to access this file")
		return is_owner
		
	def set_delivered_biosample(self, serial, status, delivery_tx):
		self.biosample.set_delivered_biosample(serial, status, delivery_tx)

	def validate_ownership(self, owner, biosample_serial):
			biosample = self.biosample.find_all_by_owner(owner, biosample_serial)

	def expression_to_list (self, list_expression):
			try:
					if '-' in list_expression:
							start, end = map(int, list_expression.strip("[]").split('-'))
							return list(range(start, end + 1))
					else:
							return sorted(map(int, list_expression.strip("[]").split(', ')))
			except:
					raise Exception(f"Syntax error in biosample list expression: '{list_expression}' must be list or range")
			
	def expression_to_range(self, _range:str, _limit:int):
			_range = _range.replace('[', '').replace(']', '')
			if ':' in _range:
					parts = _range.split(':')
					start = parts[0]
					end = parts[1]
			else:
					end = _range
					start = ''

			start = int(start) - 1 if start and (not int(start) == 1) else 0
			end = int(end) if end else _limit

			if start > end:
					raise ValueError(f"NO valid range: start value higher than end value ; [{start}:{end}]")


			print("START: ", start, "   END: ", end)

			if start > _limit or end > _limit  or start > end:
					raise ValueError(f"Rango inválido: starts in: {start}, and ends in: {end}")

			return start, end
	

	def object_to_biosample(self, object):
		return {
			"serial": object.get("serial"),
			"actor": object.get("actor"),
			"owner": object.get("owner"),
			"status": object.get("status"),
			"chainID": object.get("chainID"),
			"tokenId": object.get("tokenId"),
			"files_count": object.get("files_count"),
			"transferable": object.get("transferable"),
			"txHash": object.get("txHash"),
			"txStatus": object.get("txStatus"),
			"createdAt": object.get("createdAt"),
			"updatedAt": object.get("updatedAt")
		}
	

	def object_list_to_biosample (self, object_list):
		biosamples = []
		for object in object_list:
			biosamples.append(self.object_to_biosample(object))
		return biosamples


