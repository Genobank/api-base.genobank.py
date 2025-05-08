import binascii
import datetime
import hmac
import json
import os
import re
from pprint import pprint

import eth_keys
import eth_utils
from eth_account.messages import encode_defunct
from pymongo import MongoClient
from web3 import HTTPProvider, Web3
from web3.middleware import geth_poa_middleware

from libs import json_helper_dao, mongo_helper_dao


class biosample_dao:
    def __init__(self):
        self.mongo_db_helper = mongo_helper_dao.json_helper_dao()
        self.json_helper_dao = json_helper_dao.json_helper_dao()

        self.w3 = Web3(HTTPProvider(os.getenv("CUSTOM_PROVIDER")))
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.account = self.w3.eth.account.privateKeyToAccount(
            os.getenv("BIOSAMPLE_EXECUTOR")
        )
        self.w3.eth.default_account = self.account.address
        self.SM_BPT_JSONINTERFACE = self.load_smart_contract(os.getenv("ABI_BPT_PATH"))
        self.client = MongoClient(os.getenv("MONGO_DB_HOST"))
        self.db = self.client[os.getenv("DB_NAME")]
        self.biosample_activations_table = self.db["biosample-activations"]
        self.biosamples_table = self.db["biosamples"]
        self.permissions_table = self.db["permissions"]
        self.table = self.db["biosamples"]
        self.table_deliveries = self.db["deliveries"]
        self.table_transfer_history = self.db["biosample-transfer-history"]

    def find_files_by_biosample_serial(self, biosample_serial):
        cur = self.table_deliveries.find(
            {"biosample_serial": int(biosample_serial)}
        ).sort("createdAt", -1)
        return self.json_helper_dao.serialize_cur(cur)

    def load_smart_contract(self, path):
        solcOutput = {}
        try:
            with open(path) as inFile:
                solcOutput = json.load(inFile)
        except Exception as e:
            print(f"ERROR: Could not load file {path}: {e}")
        return solcOutput

    def fetch(self, _filter={}, _projection={}):
        cur = self.table.find(_filter, _projection).sort("createdAt", -1)
        return self.mongo_db_helper.serialize_cur(cur)

    def find_all(self):
        cur = self.table.find().sort("createdAt", -1)
        return self.mongo_db_helper.serialize_cur(cur)

    def fetch_biosamples_dynamic_filter(self, filter_criteria):
        field, value = next(iter(filter_criteria.items()))
        biosamples_fields = [
            "owner",
            "status",
            "chainID",
        ]  # Ejemplo de campos específicos de biosamples
        biosample_activations_fields = [
            "permitteeSerial",
            "physicalId",
        ]  # Ejemplo de campos específicos de biosample-activations

        pipeline = []

        if field in biosamples_fields:
            pipeline.append({"$match": {field: value}})

        if field in biosample_activations_fields or field == "serial":
            pipeline.extend(
                [
                    {
                        "$lookup": {
                            "from": "biosample-activations",
                            "localField": "serial",
                            "foreignField": "serial",
                            "as": "activation_data",
                        }
                    },
                    {"$unwind": "$activation_data"},
                    {"$match": {f"activation_data.{field}": value}},
                ]
            )

        pipeline.append({"$group": {"_id": "$_id", "document": {"$first": "$$ROOT"}}})
        pipeline.append({"$replaceRoot": {"newRoot": "$document"}})

        result = self.biosamples_table.aggregate(pipeline)

        return self.mongo_db_helper.serialize_cur(result)

    def find_by_serial_and_owner(self, serial, owner):
        doc = self.table.find_one(
            {"serial": int(serial), "owner": re.compile(owner, re.IGNORECASE)}
        )
        return self.mongo_db_helper.serialize_doc(doc)

    def find_all_by_permittee_serial(self, filter):
        custom_filter = json.loads(filter)
        if not isinstance(custom_filter, dict):
            raise ValueError("Filter must be a dictionary")
        cur = self.table.find(custom_filter)
        return self.mongo_db_helper.serialize_cur(cur)

    def claim(self, token_id, data):
        biosample_id = int(token_id[0:14], 16)
        address = f"""0x{token_id[24:]}"""
        receiverAddress = Web3.toChecksumAddress(address)
        activation = self.find_by_serial(biosample_id)
        signature = data["signature"]
        seed = data["seed"]
        signature_kind = int(data["signatureKind"])
        if activation["isPersistent"]:
            if not self.check_biosample_activation_secret(data, biosample_id):
                raise Exception("Error: Invalid Signature")
        else:
            if not self.check_biosample_secret(data, biosample_id):
                raise Exception("Error: Invalid Signature")
        token_id_str, tokenmint_hash, token_perm_hash = self.claim_sm_tokens(
            token_id, receiverAddress, signature, seed, signature_kind
        )
        now = datetime.datetime.now()
        iso_time = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-4] + "Z"
        time_stamp = datetime.datetime.timestamp(now)
        data_to_sign = f"{os.getenv('NAMESPACE')}.login-third-party|{biosample_id}|{activation['permitteeSerial']}|${iso_time}"
        message = encode_defunct(text=data_to_sign)
        data_signed = self.w3.eth.account.sign_message(
            message, os.getenv("BIOSAMPLE_EXECUTOR")
        )
        data_signature = data_signed.signature.hex()
        data_hash = data_signed.messageHash.hex()
        biosample_object = {
            "serial": biosample_id,
            "actor": str(self.account.address),
            "owner": str(receiverAddress),
            "sex":data["sex"],
            "status": "ACTIVE",
            "chainID": 43113,
            "tokenId": token_id_str,
            "createdAt": datetime.datetime.now(),
            "updatedAt": datetime.datetime.now(),
            "txHash": str(tokenmint_hash).lower(),
            "txStatus": 1,
        }
        permission_object = {
            "biosampleSerial": str(biosample_id),
            "permitteeSerial": activation["permitteeSerial"],
            "actor": str(receiverAddress),
            "owner": str(receiverAddress),
            "tokenId": f"0x{token_id}",
            "status": "ACTIVE",
            "chainID": 43113,
            "createdAt": datetime.datetime.now(),
            "updatedAt": datetime.datetime.now(),
            "txHash": str(token_perm_hash),
            "txStatus": 1,
        }
        biosample_created = self.create_db_biosample(biosample_object)
        if not biosample_created:
            raise Exception("Error biosample not created")
        permission_created = self.create_db_permission(permission_object)
        if not permission_created:
            raise Exception("Error permission not created")
        return {
            "data": {
                "biosampleSerial": biosample_id,
                "hash": data_hash,
                "permitteeSerial": activation["permitteeSerial"],
                "signature": data_signature,
                "timestamp": time_stamp,
                "transactions": [
                    {"transactionHash": tokenmint_hash},
                    {"transactionHash": token_perm_hash},
                ],
            }
        }

    def create_db_biosample(self, _biosample_fields):
        inserted = self.biosamples_table.insert_one(_biosample_fields)
        return inserted.inserted_id

    def create_db_permission(self, _permission_fields):
        inserted = self.permissions_table.insert_one(_permission_fields)
        return inserted.inserted_id

    def check_biosample_activation_secret(self, data, biosample_id):
        try:
            message = str(biosample_id)
            s_hash = data["biosampleSecret"]
            hmac1 = hmac.new(
                os.getenv("BIOSAMPLE_ACTIVATION_SECRET").encode("utf-8"),
                msg=message.encode(),
                digestmod="sha256",
            )
            digest = str(hmac1.hexdigest())
            return s_hash == digest
        except Exception as e:
            raise e

    def check_biosample_secret(self, data, biosample_id):
        try:
            message = str(biosample_id)
            s_hash = data["biosampleSecret"]
            hmac1 = hmac.new(
                os.getenv("APP_SECRET").encode("utf-8"),
                msg=message.encode(),
                digestmod="sha256",
            )
            digest = str(hmac1.hexdigest())
            return s_hash == digest
        except Exception as e:
            raise e

    def claim_sm_tokens(self, _tokenId, receiver_address, sign, seed, signature_kind):
        nonce = self.w3.eth.getTransactionCount(self.account.address, 'pending')
        createTokenId_aux = f"0x{_tokenId[0:12]}000000000000{self.account.address[2:]}"
        createTokenId = int(createTokenId_aux, 16)
        contract = self.w3.eth.contract(
            address=os.getenv("BPT_CONTRACT"), abi=self.SM_BPT_JSONINTERFACE["abi"]
        )
        create_token_tx = contract.functions.mint(
            createTokenId, receiver_address, "ACTIVE"
        ).buildTransaction(
            {
                "nonce":  nonce
            }
        )
        create_token_tx_signed_tx = self.w3.eth.account.signTransaction(
            create_token_tx, private_key=os.getenv("BIOSAMPLE_EXECUTOR")
        )
        create_token_tx_hash = self.w3.eth.sendRawTransaction(
            create_token_tx_signed_tx.rawTransaction
        )
        self.w3.eth.waitForTransactionReceipt(create_token_tx_hash)
        mint_token_hash = create_token_tx_hash.hex()
        sig = Web3.toBytes(hexstr=sign[2:])
        (v, r, s) = Web3.toInt(sig[-1]), Web3.toHex(sig[:32]), Web3.toHex(sig[32:64])
        tx_send = contract.functions.createWithSignature(
            int(_tokenId, 16), "ACTIVE", int(seed, 16), r, s, v, signature_kind
        ).buildTransaction(
            {
                "nonce": nonce + 1
            }
        )
        tx_send_signed_tx = self.w3.eth.account.signTransaction(
            tx_send, private_key=os.getenv("BIOSAMPLE_EXECUTOR")
        )
        tx_send_tx_hash = self.w3.eth.sendRawTransaction(
            tx_send_signed_tx.rawTransaction
        )
        self.w3.eth.waitForTransactionReceipt(tx_send_tx_hash)
        signed_token_hash = tx_send_tx_hash.hex()
        print("tx_send_tx_hash\n", tx_send_tx_hash.hex())
        return createTokenId_aux, mint_token_hash, signed_token_hash

    def parse_address_to_int(self, address):
        try:
            valid_toke_address = Web3.toChecksumAddress(address)
        except:
            raise Exception("No valid address")

    def find_by_serial(self, serial):
        cur = self.biosample_activations_table.find_one({"serial": serial})
        cur["isPersistent"] = self.is_persistent(cur)
        return cur

    def is_persistent(self, mongo_object):
        _id = mongo_object.get("_id")
        return bool(_id)

    def find_biosample_by_serial(self, serial):
        serial = int(serial)
        doc = self.biosamples_table.find_one({"serial": serial})
        return self.mongo_db_helper.serialize_doc(doc)

    def find_biosample_details_by_serial(self, serial):
        serial = int(serial)
        pipeline = [
            {"$match": {"serial": serial}},
            {
                "$lookup": {
                    "from": "biosample-activations",
                    "localField": "serial",
                    "foreignField": "serial",
                    "as": "activations",
                }
            },
            {
                "$unwind": "$activations"  # Descompone el array para poder trabajar con los documentos individualmente
            },
            {
                "$addFields": {
                    "activations.permitteeSerialInt": {
                        "$toInt": "$activations.permitteeSerial"  # Convierte permitteeSerial a entero
                    }
                }
            },
            {
                "$lookup": {
                    "from": "profiles",
                    "localField": "activations.permitteeSerialInt",
                    "foreignField": "serial",
                    "as": "activations.profileDetails",
                }
            },
            {
                "$group": {  # Reagrupa los documentos para reconstruir la estructura original
                    "_id": "$_id",
                    "originalDocument": {"$first": "$$ROOT"},
                    "activations": {"$push": "$activations"},
                }
            },
            {
                "$replaceRoot": {  # Restaura la estructura del documento
                    "newRoot": {
                        "$mergeObjects": [
                            "$originalDocument",
                            {"activations": "$activations"},
                        ]
                    }
                }
            },
        ]
        result = self.biosamples_table.aggregate(pipeline)
        return self.mongo_db_helper.serialize_cur(list(result))

    def find_serializable_biosample_by_serial(self, serial):
        serial = int(serial)
        doc = self.biosamples_table.find_one({"serial": serial})
        return self.mongo_db_helper.serialize_doc(doc)

    def set_delivered_biosample(self, serial, status, delivery_tx):
        self.table.update_one({"serial": int(serial)}, {"$set": {"delivered": status}})
        self.table.update_one(
            {"serial": int(serial)}, {"$set": {"delivery_tx": delivery_tx}}
        )
        return True

    def cur_to_scheme(self, cur):
        if "_id" in cur:
            del cur["_id"]
        return cur

    def cur_list_to_scheme(self, curlist):
        new_list = []
        for cur in curlist:
            new_list.append(self.cur_to_scheme(cur))
        return {"data": new_list}

    def fetch_bisample_transfer_history(self, _filter={}, projection=None, exclude=True, skip=0, limit=0, sort=[("createdAt", -1)], **kwargs):
        if projection:
            projection = {field: 0 if exclude else 1 for field in projection}
        cur = self.table_transfer_history.find(_filter, projection=projection, skip=skip, limit=limit, sort=sort, **kwargs)
        return self.json_helper_dao.serialize_cur(cur)