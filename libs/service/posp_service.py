from libs.dao import posp_dao
from libs.exceptions import DomainInjectionError


class posp_service:
    def __init__(self, _posp):
        if not isinstance(_posp, posp_dao.posp_dao):
            raise DomainInjectionError.DomainInjectionError("posp_service", "posp")
        self.posp = _posp

    def create_sm_token(self, _metadata):
        sm_token = self.posp.create_sm_token(_metadata)
        if not sm_token:
            raise Exception("Error creating token manager")
        return sm_token

    def mint_posp_or_fail(self, posp_metadata):
        token_exist = self.get_posp_token(
            posp_metadata["lab_address"], posp_metadata["user_address"]
        )
        posp_metadata["token_sm"] = token_exist[1]
        token_exist = token_exist[0]
        if token_exist[0] != 0:
            raise Exception("This user already has your PoSP")
        token_hash = self.posp.mint_posp(posp_metadata)
        if not token_hash:
            raise Exception("Error during token minting")
        return token_hash

    def mint_posp_auto(self, lab_address, user_address):
        token_sm = self.posp.get_token_sm(lab_address)
        if int(token_sm, 16) > 0:
            _posp_metadata = {
                "user_address": user_address,
                "lab_address": lab_address,
                "title": "Welcome",
                "msg": "Welcome to the metaverse",
            }
            token_hash = self.mint_posp(_posp_metadata)
            if token_hash:
                _json_metadata = {}
                _json_metadata["user_address"] = user_address
                _json_metadata["lab_address"] = lab_address
                _json_metadata["hash"] = token_hash
                return _json_metadata
        else:
            return False

    def mint_posp_airdrop_from_list(self, lab_address, user_address):
        token_sm = self.posp.get_token_sm(lab_address)
        if int(token_sm, 16) > 0:
            _posp_metadata = {
                "user_address": user_address,
                "lab_address": lab_address,
                "title": "Welcome",
                "msg": "Welcome to the metaverse",
            }
            token_hash = self.mint_posp(_posp_metadata)
            if token_hash:
                _json_metadata = {}
                _json_metadata["user_address"] = user_address
                _json_metadata["lab_address"] = lab_address
                _json_metadata["hash"] = token_hash
                return _json_metadata
        else:
            raise Exception("Token Does Not Exist")

    def mint_posp(self, posp_metadata):
        token_exist = self.get_posp_token(
            posp_metadata["lab_address"], posp_metadata["user_address"]
        )
        posp_metadata["token_sm"] = token_exist[1]
        token_exist = token_exist[0]
        if token_exist[0] != 0:
            return False
        else:
            token_hash = self.posp.mint_posp(posp_metadata)
        if not token_hash:
            raise Exception("Error during token minting")
        return token_hash

    def save_posp_hash(self, metadata):
        saved = self.posp.save_posp_hash(metadata)
        if not saved:
            raise Exception("Error during saving posp hash")
        return saved

    def reset_posp_db(self):
        reset = self.posp.reset_posp_db()
        if not reset:
            raise Exception("Error during reset posp database")
        return reset

    def get_posp_token(self, lab_address, user_address):
        token_sm = self.posp.get_token_sm(lab_address)
        if int(token_sm, 16) > 0:
            token = self.posp.get_posp_token(token_sm, lab_address, user_address)
            return token, token_sm
        else:
            return [0, 0, 0, 0, 0], token_sm

    def get_all_users(self):
        all_users = self.posp.get_all_users()
        return all_users

    def find_token_by_permittee(self, _permittee):
        token_sm = self.posp.find_token_by_permittee(_permittee)
        if not token_sm:
            return False
        return token_sm

    def validate_posp(self, posp_metadata):
        if "title" not in posp_metadata:
            raise Exception("Error metadata has not title")
        if "msg" not in posp_metadata:
            raise Exception("Error metadata has not a msg")
        if "user_address" not in posp_metadata:
            raise Exception("Error metadata has not user_address")
        if "lab_address" not in posp_metadata:
            raise Exception("Error metadata has not lab_address")
        if "signature" not in posp_metadata:
            raise Exception("Error metadata has not signature")
        if "filename" not in posp_metadata:
            raise Exception("Error metadata has not filename")
        return True
