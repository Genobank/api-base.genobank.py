import base64
import binascii
import datetime
import gzip
import hmac
import io
import json
import logging
import os
import os.path
import re
import sys
import zipfile

import boto3
import web3
from boto3.s3.transfer import S3Transfer, TransferConfig
from botocore.config import Config
from botocore.exceptions import ClientError
from cherrypy.lib import static
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from eth_account.messages import encode_defunct
from pymongo import MongoClient
from web3 import HTTPProvider, Web3
from web3.auto import w3
from web3.middleware import geth_poa_middleware

from libs import json_helper_dao, mongo_helper_dao
from libs.dao import bucket_dao
from libs.dao.signature_dao import signature_dao


class genotype_dao:
    def __init__(self):
        self.w3 = Web3(HTTPProvider(os.getenv("CUSTOM_PROVIDER")))
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.account = self.w3.eth.account.privateKeyToAccount(
            os.getenv("BIOSAMPLE_EXECUTOR")
        )
        self.w3.eth.default_account = self.account.address
        self.SM_JSONINTERFACE = self.load_smart_contract(
            os.getenv("ABI_BIOSAMPLE_PATH")
        )
        self.client = MongoClient(os.getenv("MONGO_DB_HOST"))
        self.db = self.client[os.getenv("DB_NAME")]
        self.table = self.db.genotypes
        self.buckets_table = self.db.buckets
        self.ancestry_table = self.db.ancestry
        self.mongo_db_helper = mongo_helper_dao.json_helper_dao()
        self.json_helper_dao = json_helper_dao.json_helper_dao()
        self.signture_dao = signature_dao()
        self.bucket_dao = bucket_dao.bucket_dao()

    def load_smart_contract(self, path):
        solcOutput = {}
        try:
            with open(path) as inFile:
                solcOutput = json.load(inFile)
        except Exception as e:
            print(f"ERROR: Could not load file {path}: {e}")
        return solcOutput

    def mint_nft(self, metadata):
        try:
            serial = str(metadata["snps"])
            owner = str(metadata["userAddress"])
            expiration = datetime.datetime.now() + datetime.timedelta(days=365)
            expiration_timestamp = int(expiration.timestamp())
            contract = self.w3.eth.contract(
                address=os.getenv("BIOSAMPLE_COTRACT"), abi=self.SM_JSONINTERFACE["abi"]
            )
            tx = contract.functions.uploadFile(
                serial, owner, expiration_timestamp
            ).buildTransaction(
                {
                    "nonce": self.w3.eth.getTransactionCount(
                        self.account.address, "pending"
                    ),
                }
            )
            gas_estimate = self.w3.eth.estimateGas(tx)
            tx["gas"] = gas_estimate
            signed_tx = self.w3.eth.account.signTransaction(
                tx, private_key=os.getenv("BIOSAMPLE_EXECUTOR")
            )
            tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
            self.w3.eth.waitForTransactionReceipt(tx_hash)
            print("\n\n\n", tx_hash.hex(), "\n\n\n")
            return tx_hash.hex()
        except:
            raise

    def mint(self, file_name, owner, expiration_timestamp):
        try:
            contract = self.w3.eth.contract(
                address=os.getenv("BIOSAMPLE_COTRACT"), abi=self.SM_JSONINTERFACE["abi"]
            )
            tx = contract.functions.uploadFile(
                file_name, owner, expiration_timestamp
            ).buildTransaction(
                {
                    "nonce": self.w3.eth.getTransactionCount(
                        self.account.address, "pending"
                    ),
                }
            )
            gas_estimate = self.w3.eth.estimateGas(tx)
            tx["gas"] = gas_estimate
            signed_tx = self.w3.eth.account.signTransaction(
                tx, private_key=os.getenv("BIOSAMPLE_EXECUTOR")
            )
            tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
            self.w3.eth.waitForTransactionReceipt(tx_hash)
            print("\n\n\n", tx_hash.hex(), "\n\n\n")
            return tx_hash.hex()
        except:
            raise

    def share_nft(self, file_hash, owner, permittee):
        try:
            hash = int(file_hash[2:], 16)
            expiration = datetime.datetime.now() + datetime.timedelta(days=365)
            expiration_timestamp = int(expiration.timestamp())
            contract = self.w3.eth.contract(
                address=os.getenv("BIOSAMPLE_COTRACT"), abi=self.SM_JSONINTERFACE["abi"]
            )
            tx = contract.functions.shareFile(
                hash, owner, permittee, expiration_timestamp
            ).buildTransaction(
                {
                    "nonce": self.w3.eth.getTransactionCount(
                        self.account.address, "pending"
                    ),
                }
            )
            gas_estimate = self.w3.eth.estimateGas(tx)
            tx["gas"] = gas_estimate
            signed_tx = self.w3.eth.account.signTransaction(
                tx, private_key=os.getenv("BIOSAMPLE_EXECUTOR")
            )
            tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
            self.w3.eth.waitForTransactionReceipt(tx_hash)
            print("\n\n\n", tx_hash.hex(), "\n\n\n")
            return tx_hash.hex()
        except:
            raise

    def share_dataset_file(self, metadata):
        try:
            serial = str(metadata["snps"])
            owner = str(metadata["userAddress"])
            expiration = datetime.datetime.now() + datetime.timedelta(days=365)
            expiration_timestamp = int(expiration.timestamp())

            print(f"serial:{serial}")
            print(f"owner:{owner}")
            print(f"expiration:{expiration}")
            print(f"expiration_timestamp:{expiration_timestamp}")

            contract = self.w3.eth.contract(
                address=os.getenv("BIOSAMPLE_COTRACT"), abi=self.SM_JSONINTERFACE["abi"]
            )
            tx = contract.functions.uploadFile(
                serial, owner, expiration_timestamp
            ).buildTransaction(
                {
                    "nonce": self.w3.eth.getTransactionCount(
                        self.account.address, "pending"
                    ),
                }
            )
            gas_estimate = self.w3.eth.estimateGas(tx)
            tx["gas"] = gas_estimate
            signed_tx = self.w3.eth.account.signTransaction(
                tx, private_key=os.getenv("BIOSAMPLE_EXECUTOR")
            )
            tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
            self.w3.eth.waitForTransactionReceipt(tx_hash)
            print("\n\n\n", tx_hash.hex(), "\n\n\n")
            return tx_hash.hex()
        except:
            raise

    def save_db_file(self, data):
        try:
            if isinstance(data["key"], str):
                data["key"] = bytes(data["key"], "utf-8")

            _fields = {
                "owneraddr": str(data["userAddress"]).upper(),
                "filename": data["filename"],
                "original_filename": data["original_filename"],
                "genetic_test": data["genetic_test"],
                "extension": data["extension"],
                "key": data["key"],
                "consents": data["agreements"],
                "signature": data["signature"],
                "status": True,
                "filesigned": data["filesigned"],
                "filesize": data["filesize"],
                "hash": data["token_hash"],
                "stake_nfts": {},
                "tag": data.get("tag", "test"),
                "created": datetime.datetime.now(),
                "updated": datetime.datetime.now(),
            }
            self.table.insert_one(_fields)
            return True
        except:
            raise

    def fetch(self, _filter={}):
        cur = self.table.find(_filter).sort("createdAt", -1)
        return self.json_helper_dao.serialize_cur(cur)

    def find_ancestry_db(self, filename, owner, laboratory):
        cur = self.ancestry_table.find_one(
            {
                "filename": filename,
                "owner": re.compile(owner, re.IGNORECASE),
                "laboratory": re.compile(laboratory, re.IGNORECASE),
            }
        )
        if not cur:
            return False
        return cur["results"]

    def save_ancestry_db(self, genotype_info, result):
        try:
            _fields = {
                "owner": str(genotype_info["owneraddr"]).upper(),
                "laboratory": str(genotype_info["labaddr"]).upper(),
                "filename": genotype_info["filename"],
                "extension": genotype_info["extension"],
                "results": result,
                "created": datetime.datetime.now(),
                "updated": datetime.datetime.now(),
            }
            self.ancestry_table.insert_one(_fields)
            return True
        except:
            raise

    def save_file(self, file, data):
        try:
            file.file.seek(0)
            ext = data["extension"]
            file_name = data["filename"]
            fernet = Fernet(data["key"])
            content_file = file.file.read()
            encrypted_file = fernet.encrypt(content_file)
            with open(f"storage/genotypes/{file_name}." + ext, "wb") as f:
                f.write(encrypted_file)
            return file_name
        except:
            raise

    def download_file(self, name, ext):
        try:
            collection = self.db.genotypes
            cur = collection.find_one({"filename": name})
            file_path = os.path.abspath("storage/genotypes/" + name + "." + ext)
            key = cur["key"]
            key = bytes(key)
            fernet = Fernet(key)
            with open(file_path, "rb") as enc_file:
                encrypted = enc_file.read()
            decrypted = fernet.decrypt(encrypted)
            return decrypted
        except Exception as e:
            print(e)
            return False

    def download_dataset_from_bucket(self, name, ext):
        try:
            collection = self.db.genotypes
            cur = collection.find_one({"filename": name})
            key = cur["key"]
            fernet = Fernet(key)
            s3_client = boto3.client(
                service_name="s3",
                aws_access_key_id=os.getenv("BUCKET_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("BUCKET_SECRET_ACCESS_KEY_ID"),
            )
            file_key = os.getenv("BUCKET_PATH") + "/" + name
            response = s3_client.get_object(
                Bucket=os.getenv("BUCKET_NAME"), Key=file_key
            )["Body"].read()
            decrypted = fernet.decrypt(response)
            return decrypted
        except Exception as e:
            raise e

    # def stream_dataset_from_bucket(self, name, ext):
    #     try:
    #         collection = self.db.genotypes
    #         cur = collection.find_one({"filename": name})
    #         key = cur["key"]
    #         fernet = Fernet(key)
    #         s3_client = boto3.client(
    #             service_name="s3",
    #             aws_access_key_id=os.getenv("BUCKET_ACCESS_KEY_ID"),
    #             aws_secret_access_key=os.getenv("BUCKET_SECRET_ACCESS_KEY_ID"),
    #         )
    #         file_key = os.getenv("BUCKET_PATH") + "/" + name
    #         print(os.getenv("BUCKET_NAME"))
    #         s3_response = s3_client.get_object(
    #             Bucket=os.getenv("BUCKET_NAME"), Key=file_key
    #         )
    #         encrypted_data = s3_response["Body"].read()

    #         decrypted_data = fernet.decrypt(encrypted_data)

    #         def file_stream():
    #             chunk_size = 1024 * 1024  # 1 MB
    #             for i in range(0, len(decrypted_data), chunk_size):
    #                 yield decrypted_data[i : i + chunk_size]

    #         return file_stream()
    #     except Exception as e:
    #         raise e


    def stream_dataset_from_bucket(self, name, ext):
        """
        Descarga el archivo en S3, lo desencripta en chunks, y lo retorna como un generador.
        name: nombre del archivo (filename).
        ext: extensión (no se usa en este ejemplo, pero lo mantengo si lo necesitas).
        """
        try:
            collection = self.db.genotypes
            cur = collection.find_one({"filename": name})
            if not cur:
                raise Exception(f"Archivo {name} no encontrado en DB")
            key = cur["key"]
            if isinstance(key, str):
                key = base64.b64decode(key)
            fernet = Fernet(key)
            s3_client = boto3.client(
                service_name="s3",
                aws_access_key_id=os.getenv("BUCKET_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("BUCKET_SECRET_ACCESS_KEY_ID"),
            )
            file_key = os.getenv("BUCKET_PATH") + "/" + name

            s3_response = s3_client.get_object(
                Bucket=os.getenv("BUCKET_NAME"),
                Key=file_key
            )
            ciphertext = s3_response["Body"].read()
            decrypted_data = fernet.decrypt(ciphertext)
            def file_stream():
                chunk_size = 1024 * 1024  # 1 MB, ajusta a tu gusto
                for i in range(0, len(decrypted_data), chunk_size):
                    yield decrypted_data[i : i + chunk_size]

            return file_stream()

        except Exception as e:
            raise e

    def stream_dataset_from_bucket_no_decryption(self, file_path):
        """
        Igual que el anterior, pero sin desencriptar (se retorna tal cual).
        """
        try:
            s3_client = boto3.client(
                service_name="s3",
                aws_access_key_id=os.getenv("BUCKET_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("BUCKET_SECRET_ACCESS_KEY_ID"),
            )
            file_key = os.getenv("BUCKET_PATH") + "/" + file_path

            s3_response = s3_client.get_object(
                Bucket=os.getenv("BUCKET_NAME"),
                Key=file_key
            )

            def file_stream():
                for chunk in s3_response["Body"].iter_chunks(chunk_size=1024*1024):
                    yield chunk

            return file_stream()

        except Exception as e:
            raise e
        
        
    # def download_dataset_from_bucket(self, name, ext):
    # 	try:
    # 		collection = self.db.genotypes
    # 		cur = collection.find_one({"filename": name})
    # 		print("\n\ncur:", cur, "\n\n")
    # 		key = cur['key']
    # 		print("\n\n\n Downloading key::", key)
    # 		fernet = Fernet(key)
    # 		s3_client = boto3.client(service_name='s3',
    # 															aws_access_key_id=os.getenv("BUCKET_ACCESS_KEY_ID"),
    # 															aws_secret_access_key=os.getenv("BUCKET_SECRET_ACCESS_KEY_ID"))
    # 		file_key = os.getenv("BUCKET_PATH") + "/" + name

    # 		# Inicializar una lista vacía para almacenar las partes desencriptadas
    # 		decrypted_parts = []

    # 		part_num = 1
    # 		while True:
    # 			try:
    # 				# Descargar cada parte
    # 				response = s3_client.get_object(Bucket=os.getenv("BUCKET_NAME"), Key=file_key, PartNumber=part_num)['Body'].read()
    # 				# Desencriptar la parte y agregarla a la lista
    # 				decrypted_part = fernet.decrypt(response)
    # 				decrypted_parts.append(decrypted_part)
    # 				part_num += 1
    # 			except s3_client.exceptions.NoSuchKey:
    # 					# Si no hay más partes, romper el bucle
    # 				break
    # 			except s3_client.exceptions.ClientError as e:
    # 				if e.response['Error']['Code'] == 'InvalidPartNumber':
    # 						# Si no hay más partes, romper el bucle
    # 					break
    # 				else:
    # 						# Si es otro error, levantar la excepción
    # 					raise e

    # 		# Combinar todas las partes desencriptadas para obtener el archivo completo
    # 		decrypted_file = b''.join(decrypted_parts)
    # 		return decrypted_file

    # 	except Exception as e:
    # 			raise e

    def upload_file_to_bucket(self, dataset_file, file_name, permittee):
        cur = self.buckets_table.find_one(
            {"permittee": re.compile(permittee, re.IGNORECASE)}
        )
        if not cur:
            exception_account = int(web3.Web3.toChecksumAddress(permittee), 16)
            acc_except = [
                119291188120719338625660708458653265813805800094,
                451629096598492253986138676752610719961088798814,
            ]
            if exception_account in acc_except:
                return True
            else:
                raise Exception("Bucket Not found")
        else:
            BUCKET_NAME = cur["bucket_name"]
            ACCESS_KEY = cur["access_key_id"]
            SECRET_KEY = cur["secret_access_key"]
            dataset_file.file.seek(0)
            upload_file = dataset_file.file.read()
            s3_client = boto3.client(
                service_name="s3",
                aws_access_key_id=ACCESS_KEY,
                aws_secret_access_key=SECRET_KEY,
            )
            try:
                file_name = str(file_name)
                response = s3_client.upload_fileobj(
                    io.BytesIO(upload_file), BUCKET_NAME, file_name
                )
            except ClientError as e:
                print(e)
                logging.error(e)
                return False
            return True

    def upload_dataset_to_somos_bucket(self, file, filename):
        try:
            somos_bucket = self.buckets_table.find_one({"permittee_serial": 150})
            file.seek(0)
            s3_client = boto3.client(
                service_name="s3",
                aws_access_key_id=somos_bucket["access_key_id"],
                aws_secret_access_key=somos_bucket["secret_access_key"],
            )
            response = s3_client.upload_fileobj(
                io.BytesIO(file.read()),
                somos_bucket["bucket_name"],
                "genotypes/" + str(filename),
            )
            return response
        except ClientError as e:
            print(e)
            logging.error(e)
            return False

    def exist_ancestry_from_somos_bucket(self, file_path):
        somos_bucket = self.buckets_table.find_one({"permittee_serial": 150})

        return self.bucket_dao.exist_file(
            somos_bucket["access_key_id"],
            somos_bucket["secret_access_key"],
            somos_bucket["bucket_name"],
            "results-test/" + str(file_path),
        )

    def get_ancestry_data_from_somos_bucket(self, folder):
        somos_bucket = self.buckets_table.find_one({"permittee_serial": 150})

        return self.bucket_dao.get_file(
            somos_bucket["access_key_id"],
            somos_bucket["secret_access_key"],
            somos_bucket["bucket_name"],
            "results-test/" + str(folder),
        )

    # def save_file_in_bucket(self, dataset_file, file_name, data):
    # 	s3_client = boto3.client(
    # 			service_name='s3',
    # 			aws_access_key_id=os.getenv("BUCKET_ACCESS_KEY_ID"),
    # 			aws_secret_access_key=os.getenv("BUCKET_SECRET_ACCESS_KEY_ID")
    # 	)
    # 	dataset_file.file.seek(0)

    # 	CHUNK_SIZE = 5 * 1024 * 1024  # 5 MB

    # 	fernet = Fernet(data["key"])
    # 	file_name = str(file_name)
    # 	multipart_upload = s3_client.create_multipart_upload(Bucket=os.getenv("BUCKET_NAME"), Key=os.getenv("BUCKET_PATH") + "/" + file_name)

    # 	try:
    # 			parts = []
    # 			part_num = 1
    # 			while True:

    # 					chunk = dataset_file.file.read(CHUNK_SIZE)
    # 					if not chunk:
    # 							break

    # 					encrypted_chunk = fernet.encrypt(chunk)
    # 					response = s3_client.upload_part(
    # 							Bucket=os.getenv("BUCKET_NAME"),
    # 							Key=os.getenv("BUCKET_PATH") + "/" + file_name,
    # 							PartNumber=part_num,
    # 							UploadId=multipart_upload["UploadId"],
    # 							Body=io.BytesIO(encrypted_chunk)
    # 					)
    # 					parts.append({"PartNumber": part_num, "ETag": response["ETag"]})
    # 					print("part_num::", part_num)
    # 					part_num += 1

    # 			s3_client.complete_multipart_upload(
    # 					Bucket=os.getenv("BUCKET_NAME"),
    # 					Key=os.getenv("BUCKET_PATH") + "/" + file_name,
    # 					UploadId=multipart_upload["UploadId"],
    # 					MultipartUpload={"Parts": parts}
    # 			)
    # 			return file_name

    # 	except ClientError as e:
    # 			if e.response['Error']['Code'] == 'MalformedXML':
    # 					print("Error: MalformedXML")
    # 					print("Parts:", parts)
    # 			s3_client.abort_multipart_upload(Bucket=os.getenv("BUCKET_NAME"), Key=os.getenv("BUCKET_PATH") + "/" + file_name, UploadId=multipart_upload["UploadId"])
    # 			print(e)
    # 			logging.error(e)
    # 			return False

    # old but stable function
    def save_file_in_bucket(self, dataset_file, file_name, data):
        s3_client = boto3.client(
            service_name="s3",
            aws_access_key_id=os.getenv("BUCKET_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("BUCKET_SECRET_ACCESS_KEY_ID"),
        )
        dataset_file.seek(0)
        file_name = data["filename"]
        fernet = Fernet(data["key"])
        content_file = dataset_file.read()
        encrypted_file = fernet.encrypt(content_file)
        try:
            file_name = str(file_name)
            response = s3_client.upload_fileobj(
                io.BytesIO(encrypted_file),
                os.getenv("BUCKET_NAME"),
                os.getenv("BUCKET_PATH") + "/" + file_name,
            )
            return file_name
        except ClientError as e:
            print(e)
            logging.error(e)
            return False

    def download_file_from_bucket(self, permittee, file_name):
        cur = self.buckets_table.find_one(
            {"permittee": re.compile(permittee, re.IGNORECASE)}
        )
        if not cur:
            raise Exception("No permittee found for bucket")
        BUCKET_NAME = cur["bucket_name"]
        ACCESS_KEY = cur["access_key_id"]
        SECRET_KEY = cur["secret_access_key"]
        # s3 = boto3.resource(service_name='s3',
        # 						aws_access_key_id=ACCESS_KEY,
        # 						aws_secret_access_key=SECRET_KEY)
        s3_client = boto3.client(
            service_name="s3",
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
        )
        # my_bucket = s3.Bucket(BUCKET_NAME)
        file_key = "results-test/json/" + file_name + ".json"
        try:
            response = s3_client.get_object(Bucket=BUCKET_NAME, Key=file_key)
            data = response["Body"].read()
            return data.decode("utf-8")
        except:
            return False

    def list_bucket_files(self, permittee, file_name):
        cur = self.buckets_table.find_one(
            {"permittee": re.compile(permittee, re.IGNORECASE)}
        )
        if not cur:
            raise Exception("No permittee found for bucket")
        BUCKET_NAME = cur["bucket_name"]
        ACCESS_KEY = cur["access_key_id"]
        SECRET_KEY = cur["secret_access_key"]
        s3 = boto3.resource(
            service_name="s3",
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
        )
        s3_client = boto3.client(
            service_name="s3",
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
        )
        my_bucket = s3.Bucket(BUCKET_NAME)
        if not file_name:
            for my_bucket_object in my_bucket.objects.all():
                print(my_bucket_object.key)
        else:
            s3_client.download_file(BUCKET_NAME, file_name, "suarchivo.txt")

    def find_genotype_by_owner(self, owner):
        try:
            collection = self.db.genotypes
            cur = collection.find({"owneraddr": re.compile(owner, re.IGNORECASE)})
            row = []
            for doc in cur:
                for key in doc:
                    if (
                        (not isinstance(doc[key], str))
                        or (not isinstance(doc[key], int))
                        or (not isinstance(doc[key], float))
                    ):
                        doc[key] = str(doc[key])
                row.append(doc)
            return row[0]
        except Exception as e:
            print(e)
            return False

    def find_file_list(self, owner):
        try:
            collection = self.db.genotypes
            cur = collection.find({"owneraddr": re.compile(owner, re.IGNORECASE)})
            return self.mongo_db_helper.serialize_cur(cur)
        except Exception as e:
            print(e)
            return False

    def find_genotype_by_permittee(self, permittee):
        try:
            collection = self.db.genotypes
            cur = collection.find({"labaddr": str(permittee).upper()})
            row = []
            for doc in cur:
                for key in doc:
                    if (
                        (not isinstance(doc[key], str))
                        or (not isinstance(doc[key], int))
                        or (not isinstance(doc[key], float))
                    ):
                        doc[key] = str(doc[key])
                row.append(doc)
            return row
        except Exception as e:
            print(e)
            return False

    def find_genotype_by_owner_and_filename(self, owner, filename):
        try:
            doc = self.table.find_one(
                {"owneraddr": re.compile(owner, re.IGNORECASE), "filename": filename}
            )
            return self.json_helper_dao.serialize_doc(doc)
            # for key in doc:
            #   if (not isinstance(doc[key], str)) or (not isinstance(doc[key], int)) or (not isinstance(doc[key], float)) or (not isinstance(doc[key], __dict__)):
            #     doc[key] = str(doc[key])
            # return doc
        except Exception as e:
            print(e)
            return False

    def find_genotype_by_signature(self, signature):
        try:
            collection = self.db.genotypes
            cur = collection.find({"filesigned": signature})
            row = []
            for doc in cur:
                for key in doc:
                    if (
                        (not isinstance(doc[key], str))
                        or (not isinstance(doc[key], int))
                        or (not isinstance(doc[key], float))
                    ):
                        doc[key] = str(doc[key])
                row.append(doc)
            return row[0]
        except Exception as e:
            print(e)
            return False

    def verify_signature(self, wallet, signature):
        genotype_db = self.find_genotype_by_owner(wallet)
        print("genotype", genotype_db)
        if not genotype_db:
            raise Exception("Genotype not found")
        wallet_db = web3.Web3.toChecksumAddress(str(genotype_db["owneraddr"]))
        signature_db = genotype_db["filesigned"]
        return (
            ((wallet == wallet_db) and (signature == signature_db)),
            genotype_db["filename"],
            genotype_db["extension"],
        )

    def verify_new_signature(self, wallet, signature):
        genotype_db = self.find_genotype_by_owner(wallet)
        if not genotype_db:
            raise Exception("Genotype not found")
        recovery_wallet = self.signture_dao.recover_from_signature(
            signature, os.getenv("NEW_MESSAGE")
        )
        print("\n\n\n\nOriginal wallet", wallet)
        print("\n\n\n\nrecovery_wallet", recovery_wallet)
        return (
            ((wallet == recovery_wallet)),
            genotype_db["filename"],
            genotype_db["extension"],
        )

    def real_validation(self, signed_message, msg, permittee):
        msg = encode_defunct(text=msg)
        wallet = w3.eth.account.recover_message(msg, signature=signed_message)
        return wallet == permittee

    def is_file_enable(self, filename):
        try:
            collection = self.db.genotypes
            cur = collection.find_one({"filename": filename})
            enable = cur["status"]
            return enable
        except Exception as e:
            print(e)
            return e

    def revoke_consents(self, owner, permittee):
        try:
            tx = self.burn_bio_token(owner, permittee)
            if not tx:
                raise Exception("Smartcontract: Error during revoke_consents")
            collection = self.db.genotypes
            collection.update_one(
                {"owneraddr": str(owner).upper()}, {"$set": {"status": False}}
            )
            return {"transactionHash": tx}
        except:
            # print(e)
            raise

    def burn_bio_token(self, owner, permittee):
        owner = web3.Web3.toChecksumAddress(owner)
        permittee = web3.Web3.toChecksumAddress(permittee)
        contract = self.w3.eth.contract(
            address=os.getenv("BIOSAMPLE_COTRACT"), abi=self.SM_JSONINTERFACE["abi"]
        )
        tx = contract.functions.burnToken(owner, permittee).buildTransaction(
            {"nonce": self.w3.eth.getTransactionCount(self.account.address)}
        )
        signed_tx = self.w3.eth.account.signTransaction(
            tx, private_key=os.getenv("BIOSAMPLE_EXECUTOR")
        )
        tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        self.w3.eth.waitForTransactionReceipt(tx_hash)
        return tx_hash.hex()

    # dtc validation section
    def Source(self, line):
        if "23andMe" in line:
            source = 0
        elif "Ancestry" in line:
            source = 1
        elif line.startswith("RSID"):
            source = 2
        elif "MyHeritage" in line:
            source = 3
        elif "Living DNA" in line:
            source = 4
        elif re.match("^#*[ \t]*rsid[, \t]*chr", line):
            source = 5
        elif "Genes for Good" in line:
            source = 6
        elif "PLINK" in line:
            source = 7
        else:
            source = -1
        return source

    def Is_zip(self, bytes_data):
        return zipfile.is_zipfile(bytes_data)

    def Is_gzip(self, bytes_data):
        return binascii.hexlify(bytes_data[:2]) == b"1f8b"

    def Extract_source(self, a, decode=False):
        first_line = self.Read_line(a, decode)
        return self.Source(first_line)

    def Read_line(self, file, decode):
        if decode:
            return file.readline().decode("utf8")
        else:
            return file.readline()

    def Manejador(self, dtc):
        try:
            if self.Is_gzip(dtc):
                with gzip.open(io.BytesIO(dtc), "rb") as f1:
                    source = self.Extract_source(f1, decode=True)
            elif self.Is_zip(dtc):
                with zipfile.ZipFile(io.BytesIO(dtc)) as z:
                    namelist = z.namelist()[0]
                    with z.open(namelist, "r") as f:
                        source = self.Extract_source(f1, decode=True)
            else:
                file = io.BytesIO(dtc)
                source = self.Extract_source(file, decode=True)
            return source
        except:
            raise Exception(
                "No valid File, upload a TXT dtc file, change your file and try again"
            )

    def find_all_by_table(self, table):
        try:
            collection = self.db[table]
            cur = collection.find()
            row = []
            for doc in cur:
                for key in doc:
                    if (
                        (not isinstance(doc[key], str))
                        or (not isinstance(doc[key], int))
                        or (not isinstance(doc[key], float))
                    ):
                        doc[key] = str(doc[key])
                row.append(doc)
            return row
        except Exception as e:
            print(e)
            return False

    def find_all(self):
        try:
            cur = self.table.find()
            row = []
            for doc in cur:
                for key in doc:
                    if (
                        (not isinstance(doc[key], str))
                        and (not isinstance(doc[key], int))
                        and (not isinstance(doc[key], float))
                        and (not isinstance(doc[key], dict))
                    ):
                        doc[key] = str(doc[key])
                row.append(doc)
            return row
        except Exception as e:
            print(e)
            return False

    def get_list_collection_names(self):
        try:
            return self.db.list_collection_names()
        except Exception as e:
            print(e)
            return False

    def reset_wallet(self, file_name, user_addr, permittee_addr, secret):
        if not self.checkSecret(file_name, user_addr, permittee_addr, secret):
            raise Exception("You do not have permission to call this method.")
        return "Validated"

    def checkSecret(self, f_name, usr_addr, pmtee_addr, secret):
        try:
            secret = str(secret)
            message = f_name + usr_addr + pmtee_addr
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
        try:
            secret = str(secret)
            hmac1 = hmac.new(
                os.getenv("APP_SECRET").encode("utf-8"),
                msg=message.encode(),
                digestmod="sha256",
            )
            hmac1 = str(hmac1.hexdigest())
            return hmac1 == secret
        except Exception as e:
            raise e

    def parse_shared_to_genotype(self, shared):
        genotype = self.find_genotype_by_owner_and_filename(
            web3.Web3.toChecksumAddress(shared["user"]), shared["filename"]
        )
        if not genotype:
            raise Exception("Error this shared file does not exist")
        return genotype

    def cur_to_scheme(self, cur):
        if "_id" in cur:
            del cur["_id"]
        if "owneraddr" in cur:
            del cur["owneraddr"]
        if "key" in cur:
            del cur["key"]
        if "signature" in cur:
            del cur["signature"]
        if "filesigned" in cur:
            del cur["filesigned"]
        if "stake_nfts" in cur:
            del cur["stake_nfts"]

        return cur

    def cur_list_to_scheme(self, curlist):
        new_list = []
        for cur in curlist:
            new_list.append(self.cur_to_scheme(cur))
        return {"data": new_list}
