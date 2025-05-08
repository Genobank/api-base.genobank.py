import hashlib
import hmac
import os
from enum import Enum

from magic_admin import Magic
from web3 import HTTPProvider, Web3

from libs.dao import signature_dao


class LoginMethods(Enum):
    MAGIC = 1
    SIGNATURE = 2


class UserDao:
    def __init__(self):
        self.w3 = Web3(HTTPProvider(os.getenv("CUSTOM_PROVIDER")))
        self.signature = signature_dao.signature_dao()

    def get_user_from_token(self, token, message=None):
        try:
            if token.startswith("WyI"):
                return self.recover_from_magic_token(token)
            elif token.startswith("0x"):  # Suponiendo que las firmas comienzan con "0x"
                return self.signature.recover_from_signature(token, message)
            # Add more conditions here to future authehtication methods
            else:
                raise ValueError("Tipo de token no reconocido")
        except Exception as e:
            print(f"Error al procesar el token: {e}")
            raise

    def get_email_from_token(self, token):
        try:
            if token.startswith("WyI"):
                return self.recover_email_from_magic_token(token)
            elif token.startswith("0x"):  # Suponiendo que las firmas comienzan con "0x"
                return False
            # Add more conditions here to future authehtication methods
            else:
                raise ValueError("Tipo de token no reconocido")
        except Exception as e:
            print(f"Error al procesar el token: {e}")
            raise

    def recover_from_magic_token(self, magic_token):
        magic = Magic(os.getenv("MAGIC_API_KEY"))
        try:
            magic.Token.validate(magic_token)
            issuer = magic.Token.get_issuer(magic_token)
            wallet = issuer.split(":")[2]
            return wallet
        except Exception as e:
            raise e

    def recover_email_from_magic_token(self, magic_token):
        magic = Magic(os.getenv("MAGIC_API_KEY"))
        try:
            magic.Token.validate(magic_token)
            issuer = magic.Token.get_issuer(magic_token)
            user_info_response = magic.User.get_metadata_by_issuer(issuer)
            user_info = user_info_response.data
            email = user_info.get("email")
            return email
        except Exception as e:
            raise e
        

    def get_email_from_wallet(self, wallet_address):
        magic = Magic(os.getenv("MAGIC_API_KEY"))
        try:
            # Obtener metadata usando la dirección de la wallet
            user_info_response = magic.User.get_metadata_by_public_address(wallet_address)
            user_info = user_info_response.data
            email = user_info.get("email")
            return email
        except Exception as e:
            print(f"Error getting email for wallet {wallet_address}: {e}")
            raise e


    def get_wallet_from_email(self, email):
        magic = Magic(os.getenv("MAGIC_API_KEY"))
        try:
            user_list_response = magic.User.get_users_by_email(email)
            if not user_list_response.data:
                return None
            user_issuer = user_list_response.data[0].get("issuer")
            if user_issuer and ":" in user_issuer:
                wallet = user_issuer.split(":")[-1]  # Obtener la última parte después del último ":"
                return wallet
            return None
        except Exception as e:
            print(f"Error getting wallet for email {email}: {e}")
            raise e


    def get_balance(self, address):
        wei_balance = self.w3.eth.get_balance(address)

        if not wei_balance:
            return {"WEI": 0, "ETH":0}
        print("\n\n\n", wei_balance, "\n\n\n")

        return {"WEI": wei_balance, "ETH": wei_balance / 1e18}

    def is_root(self, root_signature):
        sender_user = self.signature.recover_from_signature(
            root_signature, os.getenv("ROOT_MESSAGE")
        )
        return sender_user == os.getenv("ROOT_GENOBANK_WALLET")

    def encrypt_password_with_salt(self, password: str, salt: str) -> str:
        print("password", password)
        print("salt", salt)
        if not password:
            return ""
        try:
            # Crear un objeto HMAC usando el algoritmo SHA-1 y la sal como clave
            hmac_obj = hmac.new(
                salt.encode("utf-8"), password.encode("utf-8"), hashlib.sha1
            )
            # Convertir el resultado a una cadena hexadecimal
            hashed_password = hmac_obj.hexdigest()
            return hashed_password
        except Exception as e:
            raise e
