# from re import T
import datetime
import hmac
import io
import json
import os
import uuid
from time import sleep

import requests
import web3
from cryptography.fernet import Fernet

from libs.dao import file_dao, genotype_dao, posp_dao
from libs.exceptions import DomainInjectionError


class genotype_service:
    def __init__(self, _genotype, _posp_dao, _file_dao):
        if not isinstance(_genotype, genotype_dao.genotype_dao):
            raise DomainInjectionError.DomainInjectionError(
                "genotype_service", "genotype"
            )
        if not isinstance(_posp_dao, posp_dao.posp_dao):
            raise DomainInjectionError.DomainInjectionError("posp_service", "posp")
        if not isinstance(_file_dao, file_dao.file_dao):
            raise DomainInjectionError.DomainInjectionError("posp_service", "posp")

        self.genotype = _genotype
        self.posp = _posp_dao
        self.file = _file_dao

    def create(self, data, file):
        try:
            data["original_filename"] = data["filename"]
            data["filename"] = str(uuid.uuid4())
            data["key"] = (Fernet.generate_key()).decode("utf-8")
            data["key"] = bytes(data["key"], "utf-8")
            file_name = self.genotype.save_file_in_bucket(file, data["filename"], data)
            if not file_name:
                raise Exception("Error saving file, not file name")
            file.seek(0)
            if not data["extension"] == "txt":
                data["snps"] = data["filename"]
            token_hash = self.genotype.mint_nft(data)
            if not token_hash:
                raise Exception("Error minting token")
            data["token_hash"] = token_hash
            save_db_file = self.genotype.save_db_file(data)
            if not save_db_file:
                raise Exception("Error saving file in database")
            return {"filename": data["filename"]}
        except:
            raise

    def mint_nft(self, file_name, owner, expiration_time=None):
        if expiration_time is None:
            expiration_time = int(
                (datetime.datetime.now() + datetime.timedelta(days=365)).timestamp()
            )
        return self.genotype.mint(file_name, owner, expiration_time)

    def upload_file_to_somos_bucket(self, file, filename):
        uploaded = self.genotype.upload_dataset_to_somos_bucket(file, filename)
        return uploaded

    def exist_ancestry_from_somos_bucket(self, file_path):
        ancestry_file_data = self.genotype.exist_ancestry_from_somos_bucket(file_path)
        return ancestry_file_data

    def get_ancestry_data_from_somos_bucket(self, folder):
        ancestry_file_data = self.genotype.get_ancestry_data_from_somos_bucket(folder)
        return ancestry_file_data

    def reset_wallet(self, file_name, user_addr, permittee_addr, secret):
        resseted = self.genotype.reset_wallet(
            file_name, user_addr, permittee_addr, secret
        )
        return resseted

    def upload_file_to_bucket(self):
        # add boto to upload to the bucket
        bucket_send = self.genotype.upload_file_to_bucket(
            "55052008713979.zip", "somos-genobank"
        )
        if not bucket_send:
            raise Exception("Error uploading file to bucket")
        return {"response": bucket_send}

    def validate_file(self, file):
        f = file.file.read()
        source = self.genotype.Manejador(f)
        if source < 0:
            raise Exception("Not valid File Source")
        return source
        # print(source)

    def validate_extension(self, ext):
        if ext != "txt":
            raise Exception("Invalid extension you file needs to be a txt extension")
        return True

    def is_owner_or_die(self, filename, owner):
        is_owner = self.genotype.find_genotype_by_owner_and_filename(owner, filename)
        print("\n\n", is_owner, "\n\n")
        if not is_owner:
            raise Exception("This user is not allowed to access this file")
        return is_owner

    def validate_consents_metadata(self, data):
        if "agreements" not in data:
            raise Exception("Invalid consent metadata")
        agreements = data["agreements"]
        if "questions" not in agreements:
            raise Exception("Consent #1 is required for consent metadata")
        if "document" not in agreements:
            raise Exception("Consent #2 is required for consent metadata")
        if "read" not in agreements:
            raise Exception("Consent #3 is required for consent metadata")
        if "permission" not in agreements:
            raise Exception("Consent #4 is required for consent metadata")
        if "providing" not in agreements:
            raise Exception("Consent #5 is required for consent metadata")
        if "results" not in agreements:
            raise Exception("Consent #6 is required for consent metadata")

    def validate_snips(self, file):
        file.file.seek(0)
        lines = file.file.readlines()
        array_snips = self.file.get_snips(lines)
        exist_file = self.file.exists_snips(array_snips)
        if exist_file:
            raise Exception("This file already exists")
        return array_snips

    def save_db_snips(self, snips_array, data):
        saved_snips = self.file.save_db_snips(snips_array, data)
        if not saved_snips:
            raise Exception("Error no saved snips")
        return saved_snips

    def fetch(self, _filters={}):
        biosamples = self.genotype.fetch(_filters)
        if not biosamples:
            return []
        return biosamples

    def fetch_one(self, _filters={}):
        biosamples = self.genotype.fetch(_filters)
        if not biosamples:
            return []
        return biosamples[0]

    def find_by_owner(self, owner):
        genotype = self.genotype.find_genotype_by_owner(owner)
        if not genotype:
            return {}
        return genotype

    def find_file_list_by_owner(self, owner):
        file_list = self.genotype.find_file_list(owner)
        if not file_list:
            return {"data": []}
        else:
            return self.genotype.cur_list_to_scheme(file_list)

    def data_exist(self, owner):
        genotype = self.genotype.find_genotype_by_owner(owner)
        if not genotype:
            return 0
        else:
            return 1

    def find_by_permittee(self, owner):
        genotype = self.genotype.find_genotype_by_permittee(owner)
        if not genotype:
            return {}
        return genotype

    def get_base_data(self, genotype_object):
        if isinstance(genotype_object, list):
            for genotype in genotype_object:
                self.refactor_genotype(genotype)
            return genotype_object
        else:
            return self.refactor_genotype(genotype_object)

    def refactor_genotype(self, genotype_dict):
        if "_id" in genotype_dict:
            del genotype_dict["_id"]
        if "filesigned" in genotype_dict:
            del genotype_dict["filesigned"]
        if "hash" in genotype_dict:
            del genotype_dict["hash"]
        if "signature" in genotype_dict:
            del genotype_dict["signature"]
        if "key" in genotype_dict:
            del genotype_dict["key"]
        if "updated" in genotype_dict:
            del genotype_dict["updated"]
        return genotype_dict

    def list_to_json(self, gen_list):
        _json = {}
        for gen in gen_list:
            for key in gen:
                _json[key] = gen[key]

    def basic_reference(self, _genotype):
        if not _genotype:
            return []
        _json = {}
        _json["name"] = _genotype["filename"]
        _json["ext"] = _genotype["extension"]
        _json["status"] = _genotype["status"]
        _json["filesize"] = _genotype["filesize"]
        _json["consents"] = _genotype["consents"]
        _json["created"] = _genotype["created"]
        # _json["interpretation"] = {"ancestry":{"AFR_ESTE":1.8547,"AFR_NORTE":0.001,"AFR_OESTE":0.001,"ASIA_ESTE":0.001,"ASIA_SUR":0.001,"ASIA_SURESTE":0.001,"EUR_ESTE":0.001,"EUR_NORESTE":5.0803,"EUR_NORTE":0.001,"EUR_OESTE":0.001,"EUR_SUROESTE":65.7974,"JUDIO":15.8035,"MEDIO_ORIENTE":0.001,"OCEANIA":0.8112,"AMAZONAS":0.001,"ANDES":0.001,"MAYA":0.001,"PIMA":0.001,"ZAPOTECA":0.001,"HUICHOL":1.283,"MIXTECA":0.001,"NAHUA_OTOMI":9.3528,"TARAHUMARA":0.001,"TRIQUI":0.001,"Hp_m":None,"Hp_y":None}}
        # results = self.genotype.find_ancestry_db(_genotype["filename"], _genotype["owneraddr"], _genotype["labaddr"])
        # _json["interpretation"] = {}
        # exception_account = int(web3.Web3.toChecksumAddress(_genotype["labaddr"]), 16)

        # acc_except = [
        # 	119291188120719338625660708458653265813805800094,
        # 	451629096598492253986138676752610719961088798814
        # ]

        # if exception_account not in acc_except:
        # 	if not results:
        # 		results = self.genotype.download_file_from_bucket(_genotype["labaddr"],  _genotype["filename"] +"."+ _genotype["extension"])
        # 		if not results:
        # 			_json["interpretation"] = False
        # 			return _json
        # 		self.genotype.save_ancestry_db(_genotype, results)
        # 	_json["interpretation"] = json.loads(results)

        return _json

    def shared_list_to_genotype_list(self, shared_list):
        genotype_list = []
        if shared_list:
            for shared in shared_list:
                genotype = self.genotype.parse_shared_to_genotype(shared)
                genotype_bd = self.refactor_genotype(genotype)
                genotype_bd["consents"] = shared["agreements"]
                genotype_bd["status"] = str(str(shared["revoked"]).lower() != "true")
                genotype_bd["tx_hash"] = shared["transaction_hash"]
                genotype_list.append(genotype_bd)
        return genotype_list

    def authorize_download(self, wallet, signature):
        # signature = data["signature"]
        # wallet = data["wallet"]
        # # message = signature+wallet
        # # mark_key = hmac.new(signature.encode('utf-8'),msg=message.encode(), digestmod="sha256")
        validation, name, ext = self.genotype.verify_signature(wallet, signature)
        if not validation:
            raise Exception("Invalid signature")
        return name, ext

    def authorize_download_both_signature(self, wallet, signature):
        # signature = data["signature"]
        # wallet = data["wallet"]
        # # message = signature+wallet
        # # mark_key = hmac.new(signature.encode('utf-8'),msg=message.encode(), digestmod="sha256")
        validation, name, ext = self.genotype.verify_signature(wallet, signature)
        if not validation:
            validation_2, name, ext = self.genotype.verify_new_signature(
                wallet, signature
            )
            if not validation_2:
                raise Exception("Invalid signature")
        return name, ext

    def real_validation(self, signature, msg, permittee):
        valid = self.genotype.real_validation(signature, msg, permittee)
        if not valid:
            raise Exception("You permittee is not valid")
        return valid

    def is_file_enable(self, file_name):
        is_enable = self.genotype.is_file_enable(file_name)
        if not is_enable:
            raise Exception("This file has consents revoked")
        return is_enable

    def download_file(self, file_name, file_ext="txt"):
        return self.genotype.download_dataset_from_bucket(file_name, file_ext)

    def stream_file(self, file_name, file_ext="txt"):
        return self.genotype.stream_dataset_from_bucket(file_name, file_ext)

    def stream_file_no_decryption(self, file_path):
        return self.genotype.stream_dataset_from_bucket_no_decryption(file_path)

    def revoke_consents(self, owner, signature, permittee):
        authorized, name, ext = self.genotype.verify_signature(owner, signature)
        if not authorized:
            raise Exception("Invalid signature")
        revoked = self.genotype.revoke_consents(owner, permittee)
        # if not revoked:
        #   raise Exception("Couldn't revoke consent")
        return revoked

    def checkPermitteeSecret(self, id, address, secret):
        try:
            secret = str(secret)
            message = id + address
            hmac1 = hmac.new(
                os.getenv("APP_SECRET").encode("utf-8"),
                msg=message.encode(),
                digestmod="sha256",
            )
            hmac1 = str(hmac1.hexdigest())

            return hmac1 == secret
        except Exception as e:
            raise e

    def check_generic_secret(self, message, secret):
        checked = self.genotype.check_generic_secret(message, secret)
        if not checked:
            raise Exception("wrong password")
        return checked

    def insert_many_on_table(self, table, list):
        return self.genotype.insert_many(table, list)

    def find_all_genotypes(self):
        genotype_list = self.genotype.find_all()
        return genotype_list

    def find_all_by_table(self, table):
        if table == None or table == "":
            tables = self.genotype.get_list_collection_names()
            return {"Requires table name": tables}
        else:
            search = self.genotype.find_all_by_table(table)
            if not search:
                return []
        return search

    def format_allowed_filters(self, _filter):
        formatted_filter = {}
        if "type" in _filter:
            formatted_filter["genetic_test"] = {"$in": _filter["type"]}
        return formatted_filter

    # WARNIGN ZONE, FRO TEST ONLY
    def list_bucket_files(self, permitte, file):
        files_list = self.genotype.list_bucket_files(permitte, file)
        return files_list
