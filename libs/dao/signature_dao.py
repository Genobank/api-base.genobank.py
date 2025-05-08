import os

from eth_account import Account
from eth_account.messages import defunct_hash_message, encode_defunct
from web3.auto import w3


class signature_dao:
	def __init__(self):
		return None

	def isvalid(self, signed_message, msg, address):
		msg = encode_defunct(text=msg)
		recovered_wallet = w3.eth.account.recover_message(
							msg,
							signature=signed_message
		)
		return (recovered_wallet == address)

	def recover_from_signature(self, signed_message, msg):
		msg = encode_defunct(text=msg)
		recovered_wallet = w3.eth.account.recover_message(
						msg,
						signature=signed_message
		)
		return recovered_wallet


	def get_root_message(self):
		account = Account.from_key(os.getenv('ROOT_GENOBANK'))
		message = encode_defunct(text=os.getenv('ROOT_MESSAGE'))
		signed_message = account.sign_message(message)
		return signed_message.signature.hex()
	
	def is_root(self, root_signature):
		sender_user = self.recover_from_signature(root_signature, str(self.get_root_message()))
		return sender_user == os.getenv('ROOT_GENOBANK_WALLET')



	def sign_message_from_executor_wallet(self, message):
		account = Account.from_key(os.getenv('BIOSAMPLE_EXECUTOR'))
		message = encode_defunct(text=message)
		signed_message = account.sign_message(message)
		return signed_message.signature.hex()
	
	def sign_message_from_root_wallet(self, message):
		account = Account.from_key(os.getenv('ROOT_GENOBANK'))
		message = encode_defunct(text=message)
		signed_message = account.sign_message(message)
		return signed_message.signature.hex()

	#def is_root(self, double_signature):
	#	msg = encode_defunct(text= os.getenv("MESSAGE"))
	#	recovered_wallet = w3.eth.account.recover_message(
	#					msg,
	#					signature=double_signature
	#	)
	#	return str(recovered_wallet).upper() == str( os.getenv("ROOT_GENOBANK_WALLET")).upper

	







	
