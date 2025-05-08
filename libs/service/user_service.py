import os

import web3

from libs.dao import user_dao
from libs.exceptions import DomainInjectionError


class user_service:
    def __init__(self, _user):
        if not isinstance(_user, user_dao.UserDao):
            raise DomainInjectionError.DomainInjectionError("user_service", "user")
        self.user = _user

    def get_user_from_token(self, signature, message=None):
        return self.user.get_user_from_token(signature, message)

    def get_email_from_token(self, signature):
        return self.user.get_email_from_token(signature)

    def get_balance(self, address):
        return self.user.get_balance(address)

    def is_root(self, root_signature):
        is_root = self.user.is_root(root_signature)
        return is_root

    def encrypt_password_with_salt(self, password: str, salt: str) -> str:
        return self.user.encrypt_password_with_salt(password, salt)

    def tochecksum(self, address):
        return web3.Web3.toChecksumAddress(address)
    
    def get_email_from_wallet(self, user_address):
        return self.user.get_email_from_wallet(user_address)
    

    def get_wallet_from_email(self, email):
        return self.user.get_wallet_from_email(email)
