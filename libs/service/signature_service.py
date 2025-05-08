import hmac
import os

from libs.dao import signature_dao
from libs.exceptions import DomainInjectionError


class signature_service:
    def __init__(self, _signature):
        if not isinstance(_signature, signature_dao.signature_dao):
            raise DomainInjectionError.DomainInjectionError("signature_service", "signature")
        self.signature = _signature

    def recover_from_signature(self, signature, message):
        recovered_waller = self.signature.recover_from_signature(
                        signature,
                        message
        )
        return recovered_waller
    
    def get_root_message(self):
        return self.signature.get_root_message()
    
    def is_root_user_or_die(self, root_signature):
        is_root = self.signature.is_root(root_signature)
        return is_root
    

    def is_root_user_or_die_v2(self, root_signature):
        is_root = self.signature.is_root(root_signature)
        if not is_root:
            raise Exception ("No valid signature auth is not root user")
        return is_root
    

    def validate_secret(self, secret_hashed, text):
        try:
            hmac1 = hmac.new(
                    os.getenv('APP_SECRET').encode('utf-8'),
                    msg=text.encode(),
                    digestmod="sha256"
            )
            print("hmac1", hmac1)
            digest = str(hmac1.hexdigest())
            print("digest", digest)

            return secret_hashed == digest
        except Exception as e:
            raise e


    def sign_message_from_executor_wallet(self, message):
        return self.signature.sign_message_from_executor_wallet(message)
    
    def sign_message_from_root_wallet(self, message):
        return self.signature.sign_message_from_root_wallet(message)
    
