
import base64
import datetime
import hmac
import json
import os
import re
import time
from hmac import digest

import web3
from dotenv import load_dotenv
from eth_account.messages import encode_defunct
from pymongo import MongoClient
from web3 import HTTPProvider, Web3
from web3.auto import w3
from web3.middleware import geth_poa_middleware

from libs import mongo_helper_dao


class permittee_dao:
	def __init__(self):
		self.w3 = Web3(HTTPProvider(os.getenv('CUSTOM_PROVIDER')))
		self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
		self.account = self.w3.eth.account.privateKeyToAccount(os.getenv('BIOSAMPLE_EXECUTOR'))
		self.w3.eth.default_account = self.account.address
		self.client = MongoClient(os.getenv('MONGO_DB_HOST'))
		self.db = self.client[os.getenv('DB_NAME')]
		print(self.db)
		self.SM_JSONINTERFACE = self.load_smart_contract(os.getenv('ABI_BPT_PATH'))
		self.table = self.db.permittees
		self.mongo_db_helper = mongo_helper_dao.json_helper_dao()
		return None

	def create_permittee(self, id, address, secret):
		try:
			my_address = web3.Web3.toChecksumAddress(address)
			if not self.checkPermitteeSecret(id, my_address, secret):
				raise Exception("Invalid secret")
			token_hash = self.mint_permittee(id, my_address)
			print(token_hash)
			if not token_hash:
				raise Exception("Could not mint permittee")
			created = self.save_and_insert_in_DB(int(id), my_address, token_hash)
			if created:
				return {"data":[{"transactionHash": token_hash}]}
			else:
				return {"data":[{"transactionHash": token_hash}], "warning": "lo saved"}
		except Exception as e:
			raise e
		
	def check_sum_address(self, address):
		return web3.Web3.toChecksumAddress(address)
	
	def add_new_line(self, new_line):
		try:
			for key in new_line:
				if (not isinstance(new_line[key], str)) or (not isinstance(new_line[key], int)) or (not isinstance(new_line[key], float)):
					new_line[key] = str(new_line[key])
			with open(os.getenv('PERMITEE_INSERTS'), 'a') as f:
				f.write(json.dumps(new_line)+',\n')
			return True
		except Exception as e:
			print(e)
			return False
			
	def save_and_insert_in_DB(self, id, address, tx_hash):
		try:
			int_id = int(id)
			hex_id = hex(int_id)[2:]
			left_id = str(hex_id).zfill(12)
			token_id = '0x000000000000' + left_id + self.account.address[2:]
			_fields = {
			'serial': id,
			'actor': self.account.address,
			'owner': address,
			'chain': os.getenv('CHAIN_NAME'),
			'status': 'ACTIVE',
			'tokenId': token_id,
			'createdAt': datetime.datetime.now(),
			'updatedAt': datetime.datetime.now(),
			'txHash': tx_hash,
			'sequenceIndicator': 1
			}
			print("\n\n", _fields, "\n\n")
			print("\n\n", self.db, "\n\n")
			x = self.db.permittees.insert_one(_fields)
			return x.inserted_id
		except:
			raise

	def find_all_permittees(self):
		cur = self.table.find().sort("createdAt", -1)
		row = []
		for doc in cur:
			for key in doc:
				if (not isinstance(doc[key], str)) or (not isinstance(doc[key], int)) or (not isinstance(doc[key], float)):
					doc[key] = str(doc[key])
			row.append(doc)
		return row
	
	def load_smart_contract(self,path):
				solc_output = {}
				try:
						with open(path) as inFile:
								solc_output = json.load(inFile)
				except Exception as e:
						print(f"ERROR: Could not load file {path}: {e}")
				return solc_output

	def checkPermitteeSecret(self, id, address, secret):
		try:
			secret = str(secret)
			message=id+address
			hmac1 = hmac.new(os.getenv('APP_SECRET').encode('utf-8'),msg=message.encode(), digestmod="sha256")
			hmac1 = str(hmac1.hexdigest())
			return hmac1 == secret
		except Exception as e:
			raise e


	def mint_permittee(self, id, address):
		try:
			wallet = self.w3.eth.account.privateKeyToAccount(os.getenv('BIOSAMPLE_EXECUTOR')).address
			int_id = int(id)
			contract_address = os.getenv('BPT_CONTRACT')
			token = self.w3.eth.contract(address=contract_address, abi=self.SM_JSONINTERFACE['abi'])
			hex_id = hex(int_id)[2:]
			left_id = str(hex_id).zfill(12)
			createTokenId = '0x000000000000' + left_id + self.account.address[2:]
			id_token = int(createTokenId, 16)
			tx = token.functions.mint(id_token, address, 'ACTIVE').buildTransaction({
						'nonce': self.w3.eth.getTransactionCount(self.account.address)
			})
			signed_tx = self.w3.eth.account.signTransaction(tx, private_key=os.getenv('BIOSAMPLE_EXECUTOR'))
			tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
			tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
			return tx_hash.hex()
		except:#Exception as e:
			raise

	def get_serial_from_address(self, address):
		try:
			collection = self.db.permittees
			cur = collection.find_one({"owner": re.compile(address, re.IGNORECASE)})
			if not cur:
				return []
			return cur['serial']
		except Exception as e:
			raise

	def find_by_owner(self, address):
		try:
			cur = self.table.find_one({"owner": re.compile(address, re.IGNORECASE)})
			return cur
		except Exception as e:
			print(e)
			return False


	def validate_permittee(self, address):
		try:
			collection = self.db.permittees
			cur = collection.find_one({"owner": re.compile(address, re.IGNORECASE)})
			if not cur:
				return False
			for key in cur:
				if (not isinstance(cur[key], str)) or (not isinstance(cur[key], int)) or (not isinstance(cur[key], float)):
					cur[key] = str(cur[key])
			return cur
		except Exception as e:
			print(e)
			return e
		
	def find_all(self):
		cur = self.table.find().sort('createdAt', -1)
		return self.mongo_db_helper.serialize_cur(cur)

	def find_by_serial(self, serial:int):
		try:
			collection = self.db.permittees
			doc = collection.find_one({"serial": int(serial)})
			return self.mongo_db_helper.serialize_doc(doc)
		except Exception as e:
			print(e)
			return e

	def validate_permittee_signature(self, permittee_address, msg, signed_message):
		if not self.validate_permittee(permittee_address):
			raise Exception("Invalid permittee signature")
		msg = encode_defunct(text=msg)
		wallet = w3.eth.account.recover_message(msg, signature=signed_message)
		return (wallet == permittee_address)
	

	def get_next_enabled_serial(self):
		existing_serials = set(self.table.distinct("serial"))
		existing_serials = sorted(existing_serials)
		next_serial = 1
		while next_serial in existing_serials:
			next_serial += 1
		return next_serial
	