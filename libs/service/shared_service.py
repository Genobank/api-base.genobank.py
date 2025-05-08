import ast
import json
import re

from libs.dao import genotype_dao, shared_dao
from libs.exceptions import DomainInjectionError


class shared_service:
    def __init__(self, _shared, _genotype):
        if not isinstance(_shared, shared_dao.shared_dao):
            raise DomainInjectionError.DomainInjectionError("shared_service", "shared")
        if not isinstance(_genotype, genotype_dao.genotype_dao):
            raise DomainInjectionError.DomainInjectionError(
                "shared_service", "genotype"
            )
        self.shared = _shared
        self.genotype = _genotype

    def get_shares_by_user(self, user):
        profiles = self.shared.profile_dao.find_all()
        shares_list = self.shared.find_shares_by_user(user)
        for share in shares_list:
            share["agreements"] = ast.literal_eval(share["agreements"])
            for profile in profiles:
                if "autograph_signature" in profile:
                    del profile["autograph_signature"]
                if "autograph_signature_1" in profile:
                    del profile["autograph_signature_1"]
                if "autograph_signature_2" in profile:
                    del profile["autograph_signature_2"]

                print(share["serial"], "==", profile["serial"])
                if share["serial"] == profile["serial"]:
                    share["text"] = json.loads(profile["text"])
                    break
        return shares_list

    def get_shares_by_filehash(self, user, hash):
        profiles = self.shared.profile_dao.find_all()["data"]
        shares_list = self.shared.find_shares_by_filehash(user, hash)
        for share in shares_list:
            # share["agreements"] = ast.literal_eval(share["agreements"])
            for profile in profiles:
                if "autograph_signature" in profile:
                    del profile["autograph_signature"]
                if "autograph_signature_1" in profile:
                    del profile["autograph_signature_1"]
                if "autograph_signature_2" in profile:
                    del profile["autograph_signature_2"]

                print(share["serial"], "==", profile["serial"])
                print("\n\ntype of the fixed_json_str", type(profile["text"]))

                if int(share["serial"]) == int(profile["serial"]):
                    try:
                        fixed_json_str = profile["text"].replace("'", '"')
                        fixed_json_str = re.sub(
                            r'(https:|http:)"', r"\1//", fixed_json_str
                        )

                        share["text"] = json.loads(fixed_json_str)
                        print("\nJson loads correcto SIN ERROR")
                        print(share["text"])
                    except:
                        print("\n----------- PROFILE INCORRECT FORMAT --------------\n")

                        print("\n\nProfile text wrong", profile["text"])
                    break
        return shares_list

    def enabled_labs_by_hash(self, pmttee_lst, user, file_hash):
        shares_list = self.shared.find_shares_by_user(user, file_hash)
        enabled_list = self.shared.get_enabled_list(pmttee_lst, shares_list)
        return enabled_list

    def mint_file_or_fail(self, filename, owner, permittee):
        data = {"filename": filename, "userAddress": owner, "labAddress": permittee}
        tx_hash = self.genotype.mint_nft(data)
        if not tx_hash:
            raise Exception("Could not mint the file")
        return tx_hash

    def share_nft(self, filehash, owner, permittee):
        tx_hash = self.genotype.share_nft(filehash, owner, permittee)
        if not tx_hash:
            raise Exception("Could not mint the file")
        return tx_hash

    def share_file(self, user, data):
        data["user"] = str(user)
        saved = self.shared.share_file(data)
        if not saved:
            raise Exception("Error saving user shares")
        return saved

    def get_enabled_profiles_from_lab_list(self, enable_lab_list):
        lab_profiles = self.shared.get_enabled_profiles_from_lab_list(enable_lab_list)
        return lab_profiles

    def fix_lab_list(self, laboratory_list):
        new_list = []
        for lab in laboratory_list:
            new_list.append(self.fix_lab(lab))
        return {"data": new_list}

    def fix_lab(self, laboratory):
        if "autograph_signature_1" in laboratory:
            del laboratory["autograph_signature_1"]
        if "autograph_signature_2" in laboratory:
            del laboratory["autograph_signature_2"]

        if "autograph_signature_3" in laboratory:
            del laboratory["autograph_signature_3"]

        return laboratory

    def find_shared_files_by_lab(self, laboratory):
        shares_list = self.shared.find_shared_files_by_lab(laboratory)
        return shares_list

    def is_revoked(self, file_name, permittee):
        is_revoked = self.shared.is_revoked(file_name, permittee)
        # if is_revoked:
        # 		raise Exception("This file has consents revoked")
        return is_revoked

    def revoke_consents(self, user, permittee):
        revoked = self.shared.revoke_consents(user, permittee)
        if not revoked:
            raise Exception("Error revoking consent")
        return revoked

    def fetch(self, _filters={}):
        shared = self.shared.fetch(_filters)
        if not shared:
            return []
        return shared

    def fetch_one(self, _filters={}):
        shared = self.shared.fetch(_filters)
        if not shared:
            return []
        return shared[0]
