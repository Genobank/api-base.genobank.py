# -*- coding: UTF-8 -*-
#
# MODULE: runweb || CherryPy Server
# FILE: runweb.py
# USE: python3 start.py (at root directory)
#
# > @author
# > Francisco Tun
#
#  DESCRIPTION:
# > This is the main script for the Creator of Permittees for Genobank.io.  (Genobank.io),
# is intended to work within the blockchain network.
#
# REVISION HISTORY:
#
# 14 July 2022 - Initial Version
# -- -- 2022 - Final Version
#
# MODIFICATIONS:
#
# Initial mod. version: --------
# Final mod. version:   --------
#
# TODO_dd_mmm_yyyy - TODO_describe_appropriate_changes - TODO_name
# --------------------------------------------------------------------------

import ast
import hmac
import json
import os
from os.path import abspath

import cherrypy
from dotenv import load_dotenv
from mako.lookup import TemplateLookup
from mako.template import Template

from libs.dao import (
    biosample_activation_dao,
    biosample_dao,
    bounty_dao,
    bucket_dao,
    delivery_dao,
    download_dao,
    file_dao,
    genotype_dao,
    license_dao,
    magic_link_dao,
    pending_permittee_dao,
    permitte_dao,
    posp_dao,
    profile_dao,
    shared_dao,
    signature_dao,
    user_dao,
    variant_dao,
    xBPT_dao,
)
from libs.service import (
    biosample_activation_service,
    biosample_service,
    biosample_transfer_history_service,
    bounty_service,
    bucket_service,
    delivery_service,
    download_service,
    file_service,
    genotype_service,
    license_service,
    license_token_service,
    magic_link_service,
    pending_permittee_service,
    permittee_service,
    posp_service,
    profile_service,
    shared_service,
    signature_service,
    user_service,
    variant_service,
    xBPT_service,
)

class Server():
    def __init__(self):
        biosample = biosample_dao.biosample_dao()
        _file = file_dao.file_dao()
        genotype = genotype_dao.genotype_dao()
        licence = license_dao.license_dao()
        posp = posp_dao.posp_dao()
        permitte = permitte_dao.permittee_dao()
        pending_permittee = pending_permittee_dao.pending_permittee_dao()
        profile = profile_dao.profile_dao()
        biosample_activation = biosample_activation_dao.biosample_activation_dao()
        shared = shared_dao.shared_dao()
        signature = signature_dao.signature_dao()
        bucket = bucket_dao.bucket_dao()
        delivery = delivery_dao.delivery_dao()
        magic_link = magic_link_dao.magic_link_dao()
        user = user_dao.UserDao()
        download = download_dao.DownloadDAO()
        xbpt = xBPT_dao.XBPT_DAO()
        variant = variant_dao.VariantDAO()
        bounty = bounty_dao.BountyDAO()

        self.biosample_service = biosample_service.biosample_service(biosample)
        self.file_service = file_service.FileService(_file)
        self.genotype_service = genotype_service.genotype_service(genotype, posp, _file)
        self.licence_service = license_service.license_service(licence)
        self.posp_service = posp_service.posp_service(posp)
        self.permittee_service = permittee_service.permittee_service(permitte)
        self.pending_permittee_service = (
            pending_permittee_service.pending_permittee_service(pending_permittee)
        )
        self.profile_service = profile_service.profile_service(profile)
        self.biosample_activation_service = (
            biosample_activation_service.biosample_activation_service(
                biosample_activation
            )
        )
        self.license_token_service = license_token_service.LicenseTokenService()
        self.shared_service = shared_service.shared_service(shared, genotype)
        self.signature_service = signature_service.signature_service(signature)
        self.bucket_service = bucket_service.bucket_service(bucket)
        self.delivery_service = delivery_service.delivery_service(delivery)
        self.magic_link_service = magic_link_service.magic_link_service(magic_link)

        self.user_service = user_service.user_service(user)
        self.download_service = download_service.DownloadService(download)
        self.xbpt_service = xBPT_service.xBPT_service(xbpt)
        self.variant_service = variant_service.variantService(variant)
        self.bounty_service = bounty_service.bountyService(bounty)
        self.biosample_transfer_history_service = biosample_transfer_history_service.BiosampleTransferHistoryService()

        self.mylookup = TemplateLookup(directories=["public/pages"])
        return None

    load_dotenv()

    def jsonify_error(status, message, traceback, version):
        return json.dumps(
            {
                "status": "Failure",
                "status_details": {"message": status, "description": message},
            }
        )

    _cp_config = {"error_page.default": jsonify_error}

    # free cors
    def cors():
        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
        if cherrypy.request.method == "OPTIONS":
            cherrypy.response.headers["Access-Control-Allow-Methods"] = (
                "GET, POST, PATCH, PUT, DELETE, OPTIONS"
            )
            cherrypy.response.headers["Access-Control-Allow-Headers"] = "Content-type"
            cherrypy.response.status = 200
            return ""
        else:
            return None

    cherrypy.tools.CORS = cherrypy.Tool("before_finalize", cors)

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    def options(self, *args, **kwargs):
        print("\n\n this is an options main site")
        return 200

    # Methods -------------------------------------------------------------------
    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    def index(self):
        t = Template(filename="public/pages/index.mako")
        return t.render(message=os.getenv("ENVIROMENT"))

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["GET"])
    def adminpage(self, place=None):
        if place == None or place == "test":
            t = self.mylookup.get_template("adminpage.mako")
            return t.render(plc="AdminPage", env=os.getenv("FRONT_ENV"))
        elif place == "permittee" or place == "test-permittee":
            t = self.mylookup.get_template("adminpage.mako")
            return t.render(plc="Permittee", env=os.getenv("FRONT_ENV"))
        elif place == "profile" or place == "test-profile":
            t = self.mylookup.get_template("profiles.mako")
            return t.render(plc="Profiles", env=os.getenv("FRONT_ENV"))

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["GET"])
    def manager_dashboard(self, section=None):
        t = self.mylookup.get_template("/permittees_manager/aprove_perm.mako")
        msg = self.signature_service.get_root_message()
        return t.render(api_msg=msg, env=os.getenv("FRONT_ENV"))
    

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["GET"])
    def claude_manager(self, section=None):
        t = self.mylookup.get_template("/claude_manager/claude_manager.mako")
        msg = self.signature_service.get_root_message()
        return t.render(api_msg=msg, env=os.getenv("FRONT_ENV"))

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["GET"])
    def shop_manager(self):
        t = self.mylookup.get_template("/shop_manager/shop_manager.mako")
        msg = self.signature_service.get_root_message()
        return t.render(api_msg=msg, env=os.getenv("FRONT_ENV"))

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["GET"])
    @cherrypy.tools.json_out()
    def login(self, user_sign):
        try:
            user = self.user_service.get_user_from_token(user_sign)
            return user
        except Exception as e:
            msg = ""
            if "message" in e.args[0]:
                msg = str(e.args[0]["message"])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["GET"])
    @cherrypy.tools.json_out()
    def profiles(self, serial=None):
        try:
            if not serial:
                return self.profile_service.find_all()
            else:
                return self.profile_service.find_by_serial(serial)
        except Exception as e:
            msg = ""
            if "message" in e.args[0]:
                msg = str(e.args[0]["message"])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)
        
                
    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["GET"])
    @cherrypy.tools.json_out()
    def permittees(self, serial=None):
        try:
            if not serial:
                return {"data": self.permittee_service.find_all()}
            else:
                return {"data": self.permittee_service.find_by_serial(serial)}
        except ValueError as e:
            error_response = {
                "errors": [{"code": 400005, "message": "Invalid permittee ID."}],
                "id": "65ad6a2b54c20a0008a48d9f",  # Asegúrate de generar este ID adecuadamente
                "status": 400,
            }
            cherrypy.response.status = 400
            return error_response
        except Exception as e:
            msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["GET"])
    @cherrypy.tools.json_out()
    def biosample_activations(self, **params):
        filter_dict = params
        try:
            result = {}
            if not filter_dict:
                result["data"] = self.biosample_activation_service.find_all()
            else:
                return self.biosample_activation_service.find_all_filtered_by(
                    filter_dict
                )
            return result
        except Exception as e:
            msg = ""
            if "message" in e.args[0]:
                msg = str(e.args[0]["message"])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["GET"])
    @cherrypy.tools.json_out()
    def biosamples(self, **params):
        filter_dict = params
        if "serial" in filter_dict:
            filter_dict["serial"] = int(filter_dict["serial"])
        if "chainID" in filter_dict:
            filter_dict["chainID"] = int(filter_dict["chainID"])
        try:
            if not filter_dict:
                return self.biosample_service.find_all()
            else:
                biosample_activations = self.biosample_activation_service.find_all()
                biosamples = self.biosample_service.find_all()
                full_biosamples = self.biosample_service.fetch_biosamples_by_full_fields(
                    biosamples["data"], biosample_activations["data"]
                )
                full_biosamples_filtered = self.biosample_service.filter_biosamples(
                    full_biosamples, filter_dict
                )
                biosamples = self.biosample_service.object_list_to_biosample(
                    full_biosamples_filtered
                )
                return {"data": biosamples}
        except ValueError as e:
            error_response = {
                "errors": [
                    {
                        "code": 400005,
                        "message": "Invalid biosample ID."
                    }
                ],
                "id": "65ad6a2b54c20a0008a48d9f",
                "status": 400
            }
            cherrypy.response.status = 400
            return error_response
        except Exception as e:
            msg = ""
            if 'message' in e.args[0]:
                msg = str(e.args[0]['message'])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)


    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["GET"])
    @cherrypy.tools.json_out()
    def biosample_details(self, biosample_serial):
        try:
            biosample = self.biosample_service.find_biosample_by_serial(
                biosample_serial
            )
            if biosample:
                biosample["activation"] = (
                    self.biosample_activation_service.find_by_serial(biosample_serial)
                )
                if biosample["activation"]:
                    profile = self.profile_service.find_by_serial(
                        biosample["activation"]["permitteeSerial"]
                    )
                    permittee = self.permittee_service.find_by_serial(
                        biosample["activation"]["permitteeSerial"]
                    )
                    biosample["profile"] = profile["data"]
                    biosample["permittee"] = permittee
                file_paths = []
                delivery_files = self.delivery_service.find_by_biosample_serial(
                    int(biosample_serial)
                )
                if delivery_files:
                    if delivery_files["data"]:
                        # Extraer y extender file_paths en una sola línea
                        file_paths = [
                            value
                            for delivery in delivery_files["data"]
                            for value in (
                                delivery["files"].values()
                                if isinstance(delivery["files"], dict)
                                else delivery["files"]
                            )
                        ]
                        file_names = [path.split("/")[-1] for path in file_paths]
                        biosample["file_names"] = file_names
                biosample["blockchain_logo"] = (
                    "https://cryptologos.cc/logos/avalanche-avax-logo.png"
                )
                variants = self.variant_service.fetch(
                    {"biosampleSerial": int(biosample_serial)}
                )
                biosample["variants"] = variants
                curator = {}
                if len(variants) > 0:
                    variant = variants[0]
                    curator = self.profile_service.fetch_one(
                        {"serial": int(variant["notarizer_serial"])}
                    )
                biosample["curator"] = curator
                biosample["bounty_data"] = self.bounty_service.fetch_one(
                    {"biosample_serial": int(biosample_serial)}
                )
                biosample_transfers = self.biosample_transfer_history_service.fetch({"biosample_serial": int(biosample_serial), "status_code": 1})
                if biosample_transfers:
                    for transfer in biosample_transfers:
                        from_permittee = self.permittee_service.find_by_owner(transfer["from"])
                        transfer["from_profile"] = self.profile_service.fetch_one({"serial": int(from_permittee["serial"])})
                        to_permittee = self.permittee_service.find_by_owner(transfer["to"])
                        transfer["to_profile"] = self.profile_service.fetch_one({"serial": int(to_permittee["serial"])})

                biosample["transfers"] = biosample_transfers
            if biosample:
                biosample["token"] = {
                    "name": "Biosample Permission Token",
                    "symbol": "BPT",
                    "is_erc721": True,
                    "is_erc1155": False,
                }
                ancestry_result = self.api_somos_dao.results_service.fetch_one(
                    {"wallet": biosample.get("owner")}
                )
                if ancestry_result and ancestry_result.get("isPublic"):
                    biosample["ancestry_result"] = ancestry_result
                    registration = self.api_somos_dao.registration_service.fetch_one(
                        {"wallet": ancestry_result.get("wallet")}
                    )
                    biosample["ancestry_result"]["sex"] = registration.get("sex")
                else:
                    biosample["ancestry_result"] = []

            return biosample

        except Exception as e:
            msg = ""
            if 'message' in e.args[0]:
                msg = str(e.args[0]['message'])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)
        
    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["GET"])
    @cherrypy.tools.json_out()
    def get_owner_details(self, owner_address):
        user_address = self.user_service.tochecksum(owner_address)
        ancestry_result = self.api_somos_dao.results_service.fetch_one(
            {"wallet": user_address, "isPublic": True}
        )
        sex = None
        if ancestry_result:
            registration = self.api_somos_dao.registration_service.fetch_one(
                {"wallet": ancestry_result.get("wallet")}
            )
            sex = registration.get("sex")
        uploaded_files = self.genotype_service.fetch(
            {"owneraddr": str(user_address).upper()}
        )
        uploaded_files = self.genotype_service.get_base_data(uploaded_files)
        biosamples = self.biosample_service.fetch({"owner": user_address})
        return {
            "data": {
                "ancestry": ancestry_result,
                "sex": sex,
                "uploaded_files": uploaded_files,
                "biosamples": biosamples,
            }
        }

    @cherrypy.expose
    @cherrypy.tools.CORS()
    @cherrypy.tools.allow(methods=["POST"])
    @cherrypy.tools.json_out()
    def upload_dataset_chunk(self, chunk, chunkNumber, totalChunks, data):
        try:
            chunkNumber = int(chunkNumber)
            totalChunks = int(totalChunks)
            data = json.loads(data)

            print("DATA: ", data)

            upload_dir = os.getenv("UPLOAD_FILES_CHUNKS")
            file_path = os.path.join(upload_dir, data["filename"])

            # Guardar el fragmento temporalmente
            with open(f"{file_path}_part{chunkNumber}", "wb") as temp_chunk:
                temp_chunk.write(chunk.file.read())

            # Verificar si todos los fragmentos han sido cargados
            if all(
                os.path.exists(f"{file_path}_part{i}")
                for i in range(1, totalChunks + 1)
            ):
                # Recomponer el archivo completo
                with open(file_path, "wb") as complete_file:
                    for i in range(1, totalChunks + 1):
                        with open(f"{file_path}_part{i}", "rb") as temp_chunk:
                            complete_file.write(temp_chunk.read())
                        os.remove(f"{file_path}_part{i}")  # Eliminar fragmento temporal

                # Procesar el archivo completo como de costumbre
                self.process_uploaded_file(file_path, data)

            return {"status": "Chunk uploaded successfully"}
        except Exception as e:
            msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)

    def process_uploaded_file(self, file_path, data):
        try:
            with open(file_path, "rb") as file:
                if not data["extension"] == "txt":
                    source = -1
                else:
                    source = self.file_service.validate_file(file)
                if "extension" not in data:
                    raise Exception("This file does not have extension")
                if source >= 0:
                    self.file_service.validate_extension(data["extension"])
                    self.file_service.validate_consents_metadata(data)
                    array_snips = self.file_service.validate_snips(file)
                    data["snps"] = "".join(array_snips)
                    created = self.genotype_service.create(data, file)
                    self.genotype_service.save_db_snips(array_snips, data)
                else:
                    created = self.genotype_service.create(data, file)
                os.remove(file_path)
                return {"token": str(created)}
        except Exception as e:
            msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["GET"])
    @cherrypy.tools.json_out()
    def get_serial_permittee_by_address(self, address):
        try:
            return self.permittee_service.get_serial_from_address(address)
        except Exception as e:
            msg = ""
            if "message" in e.args[0]:
                msg = str(e.args[0]["message"])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["GET"])
    @cherrypy.tools.json_out()
    def find_file(self, signature):
        try:
            user = self.user_service.get_user_from_token(
                signature, os.getenv("MESSAGE")
            )
            file_data = self.genotype_service.find_by_owner(user)
            return self.genotype_service.basic_reference(file_data)
        except Exception as e:
            msg = ""
            if "message" in e.args[0]:
                msg = str(e.args[0]["message"])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["GET"])
    @cherrypy.tools.json_out()
    def get_my_uploaded_file_list(self, user_signature):
        try:
            user = self.user_service.get_user_from_token(
                user_signature, os.getenv("MESSAGE")
            )
            file_list = self.genotype_service.find_file_list_by_owner(user)
            if file_list:
                for file in file_list["data"]:
                    if file["extension"].upper() == "TXT":
                        # file["ancestry_json"] = (
                        #     self.genotype_service.exist_ancestry_from_somos_bucket(
                        #         "json/" + str(file["filename"]) + ".txt" + ".json"
                        #     )
                        # )
                        # file["ancestry_csv"] = (
                        #     self.genotype_service.exist_ancestry_from_somos_bucket(
                        #         "csv/" + str(file["filename"]) + ".txt" + ".csv"
                        #     )
                        # )

                        file["ancestry_json"] = []
                        file["ancestry_csv"] = []
                        print("\n file:", file)
            return file_list
        except:
            raise
        # except Exception as e:
        #     msg = ""
        #     if "message" in e.args[0]:
        #         msg = str(e.args[0]["message"])
        #     else:
        #         msg = str(e)
        #     raise cherrypy.HTTPError("500 Internal Server Error", msg)

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["GET"])
    @cherrypy.tools.json_out()
    def download_ancestry_data(self, user_signature, filename, _type):
        try:
            user = self.user_service.get_user_from_token(
                user_signature, os.getenv("MESSAGE")
            )
            genotype = self.genotype_service.fetch_one(
                {"owneraddr": str(user).upper(), "filename": filename}
            )
            if not genotype:
                raise cherrypy.HTTPError("Erro file not found")
            ancestry_data = self.genotype_service.get_ancestry_data_from_somos_bucket(
                str(_type) + "/" + str(filename) + ".txt" + "." + str(_type)
            )
            return ancestry_data
        except:
            raise
        # except Exception as e:
        #     msg = ""
        #     if 'message' in e.args[0]:
        #         msg = str(e.args[0]['message'])
        #     else:
        #         msg = str(e)
        #     raise cherrypy.HTTPError("500 Internal Server Error", msg)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def data_exist(self, owner):
        exist = self.genotype_service.data_exist(owner)
        return {"data_exists": exist}

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["GET"])
    @cherrypy.tools.json_out()
    def find_genotypes(self, signature):
        try:
            user = self.user_service.get_user_from_token(
                signature, os.getenv("MESSAGE")
            )
            return self.genotype_service.find_by_owner(user)
        except Exception as e:
            msg = ""
            if "message" in e.args[0]:
                msg = str(e.args[0]["message"])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["GET"])
    @cherrypy.tools.json_out()
    def find_genotypes_by_permittee(self, signature):
        try:
            permittee = self.user_service.get_user_from_token(
                signature, os.getenv("MESSAGE")
            )
            posp_licence = self.licence_service.find_license_by_permitte_and_type(
                permittee, 2
            )
            if posp_licence:
                posp_licence = True
            shared_list = self.shared_service.find_shared_files_by_lab(permittee)
            genotype = self.genotype_service.shared_list_to_genotype_list(shared_list)
            token = self.posp_service.find_token_by_permittee(permittee)
            bucket = self.bucket_service.has_bucket_with_permittee_address(
                str(permittee)
            )
            genotype.insert(0, bucket)
            genotype.insert(0, token)
            genotype.insert(0, posp_licence)
            return genotype
        except Exception as e:
            msg = ""
            if "message" in e.args[0]:
                msg = str(e.args[0]["message"])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    def download_file(self, wallet, signature):
        try:
            name, ext = self.genotype_service.authorize_download_both_signature(
                wallet, signature
            )
            file = self.genotype_service.download_file(name, ext)
            return file
        except Exception as e:
            msg = ""
            if "message" in e.args[0]:
                msg = str(e.args[0]["message"])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    def download_user_dashboard_file(self, signature, filename):
        try:
            owner = self.user_service.get_user_from_token(
                signature, os.getenv("MESSAGE")
            )
            self.genotype_service.is_owner_or_die(filename, owner)
            file = self.genotype_service.download_file(filename, "txt")
            return file
        except Exception as e:
            msg = ""
            if "message" in e.args[0]:
                msg = str(e.args[0]["message"])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["POST"])
    @cherrypy.tools.json_out()
    def emit_posp(self, metadata):
        try:
            _json_metadata = json.loads(metadata)
            self.posp_service.validate_posp(_json_metadata)
            name = _json_metadata["filename"]
            self.genotype_service.is_file_enable(name)
            self.permittee_service.validate_permittee_signature(_json_metadata)
            _json_metadata["hash"] = self.posp_service.mint_posp_or_fail(_json_metadata)
            self.posp_service.save_posp_hash(_json_metadata)
            return {"posp_token_hash": _json_metadata["hash"]}
        except Exception as e:
            msg = ""
            if "message" in e.args[0]:
                msg = str(e.args[0]["message"])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["POST"])
    @cherrypy.tools.json_out()
    def create_token(self, metadata):
        try:
            _jsonmetadata = json.loads(metadata)
            return self.posp_service.create_sm_token(_jsonmetadata)
        except Exception as e:
            msg = ""
            if "message" in e.args[0]:
                msg = str(e.args[0]["message"])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["GET"])
    @cherrypy.tools.json_out()
    def get_posp_token(self, lab_address, user_address):
        try:
            token_data = self.posp_service.get_posp_token(lab_address, user_address)
            return token_data[0]
        except Exception as e:
            msg = ""
            if "message" in e.args[0]:
                msg = str(e.args[0]["message"])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["POST"])
    @cherrypy.tools.json_out()
    def revoke_consents(self, signature, permittee):
        try:
            user = self.user_service.get_user_from_token(
                signature, os.getenv("MESSAGE")
            )
            revoked = self.shared_service.revoke_consents(user, permittee)
            # revoked = self.genotype_service.revoke_consents(owner, signature, permittee)
            return revoked
        except Exception as e:
            msg = ""
            if "message" in e.args[0]:
                msg = str(e.args[0]["message"])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["POST"])
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def get_permittee_requests(self):
        try:
            root_signature = cherrypy.request.json
            self.signature_service.is_root_user_or_die(root_signature["root_signature"])
            return self.pending_permittee_service.find_all_pending_permittee()
        except Exception as e:
            msg = ""
            if "message" in e.args[0]:
                msg = str(e.args[0]["message"])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["POST"])
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def reject_permittee(self, owner):
        try:
            root_signature = cherrypy.request.json
            self.signature_service.is_root_user_or_die(root_signature["root_signature"])
            self.pending_permittee_service.reject_pending_permittee_status(owner)
            return {"status": True, "text": "Permitte Rejected Successfully"}
        except Exception as e:
            msg = ""
            if "message" in e.args[0]:
                msg = str(e.args[0]["message"])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["POST"])
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def approve_permittee(self, owner):
        try:
            root_signature = cherrypy.request.json
            self.signature_service.is_root_user_or_die(root_signature["root_signature"])
            _id = self.permittee_service.get_next_enabled_serial()
            message = str(_id) + owner
            hash1 = hmac.new(
                os.getenv("APP_SECRET").encode("utf-8"),
                msg=message.encode(),
                digestmod="sha256",
            )
            self.pending_permittee_service.add_pendig_serial(owner, _id)
            new_pending_peremittee = self.pending_permittee_service.find_by_owner(owner)
            if new_pending_peremittee["status"] == 1:
                raise Exception("Error, this permittee is already approved")
            self.profile_service.create(new_pending_peremittee)
            self.permittee_service.create_permittee(str(_id), owner, hash1.hexdigest())
            self.pending_permittee_service.change_status(owner, 1)
            return {"status": True, "text": "Permitte Approved Successfully"}
        except Exception as e:
            msg = ""
            if "message" in e.args[0]:
                msg = str(e.args[0]["message"])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["POST"])
    @cherrypy.tools.json_out()
    def create_profile(self, owner):
        try:
            permittee = self.pending_permittee_service.find_by_owner(owner)
            self.profile_service.create(permittee)
            return permittee["text"]
        except Exception as e:
            msg = ""
            if "message" in e.args[0]:
                msg = str(e.args[0]["message"])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["POST"])
    @cherrypy.tools.json_out()
    def create_permitee(self, id, address, secret):
        try:
            created = self.permittee_service.create_permittee(id, address, secret)
            return created
        except Exception as e:
            msg = ""
            if "message" in e.args[0]:
                msg = str(e.args[0]["message"])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["POST"])
    @cherrypy.tools.json_out()
    def create_permitee_preregistration(self, all_data):
        try:
            json_data = json.loads(all_data)
            owner = self.user_service.get_user_from_token(
                json_data["UserSignature"], os.getenv("MESSAGE")
            )
            permittee_exist = bool(self.permittee_service.find_by_owner(owner))
            if permittee_exist:
                raise Exception("Permittee:  " + str(owner) + " is register now")
            json_data["Owner"] = owner
            return self.pending_permittee_service.create(json_data)
        except Exception as e:
            msg = ""
            if "message" in e.args[0]:
                msg = str(e.args[0]["message"])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["POST"])
    @cherrypy.tools.json_out()
    def get_all_pending_permittes(self, root_signature):
        try:
            self.signature_service.is_root_user_or_die(root_signature)
            return self.pending_permittee_service.find_all_pending_permittee()
        except Exception as e:
            msg = ""
            if "message" in e.args[0]:
                msg = str(e.args[0]["message"])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["POST"])
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def claim(self, token_id):
        try:
            data = cherrypy.request.json
            biosample_id = int(token_id[0:14], 16)
            address = f"""0x{token_id[24:]}"""
            res = self.biosample_service.claim(token_id, data)
            self.bucket_service.create_folder(
                os.getenv("BUCKET_PATH")
                + "/users/"
                + address.upper()
                + "/"
                + str(biosample_id)
                + "/"
            )

            return res
        except Exception as e:
            msg = ""
            if "message" in e.args[0]:
                msg = str(e.args[0]["message"])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)


    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["GET"])
    @cherrypy.tools.json_out()
    def validate_permittee(self, permittee):
        try:
            permittee = self.permittee_service.validate_permittee(permittee)
            permittee = self.permittee_service.basic_reference(permittee)
            return permittee
        except Exception as e:
            msg = ""
            if "message" in e.args[0]:
                msg = str(e.args[0]["message"])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["GET"])
    @cherrypy.tools.json_out()
    def get_presigned_link(self):
        try:
            link = self.bucket_service.get_presigned_bucket_file()
            return link
        except Exception as e:
            msg = ""
            if "message" in e.args[0]:
                msg = str(e.args[0]["message"])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["GET"])
    @cherrypy.tools.json_out()
    def get_shares_by_filehash(self, signature, filehash):
        try:
            user = self.user_service.get_user_from_token(
                signature, os.getenv("MESSAGE")
            )
            shares_list = self.shared_service.get_shares_by_filehash(user, filehash)
            return shares_list
        except Exception as e:
            msg = ""
            if "message" in e.args[0]:
                msg = str(e.args[0]["message"])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["GET"])
    @cherrypy.tools.json_out()
    def get_labs_enabled_to_share(self, signature, file_hash):
        try:
            user = self.user_service.get_user_from_token(
                signature, os.getenv("MESSAGE")
            )
            permitte_list = self.permittee_service.find_all_permittees()
            enable_lab_list = self.shared_service.enabled_labs_by_hash(
                permitte_list, user, file_hash
            )
            enabled_labs_profiles = (
                self.shared_service.get_enabled_profiles_from_lab_list(enable_lab_list)
            )
            fixed_labs = self.shared_service.fix_lab_list(enabled_labs_profiles["data"])
            return fixed_labs
        except Exception as e:
            msg = ""
            if "message" in e.args[0]:
                msg = str(e.args[0]["message"])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["POST"])
    def share_file(self, signature, data):
        try:
            data = json.loads(data)
            user = self.user_service.get_user_from_token(
                signature, os.getenv("MESSAGE")
            )
            tx_hash = self.xbpt_service.notarize("SHARE", json.dumps(data))
            data["tx_hash"] = tx_hash
            saved = self.shared_service.share_file(user, data)
            return saved
        except Exception as e:
            msg = ""
            if "message" in e.args[0]:
                msg = str(e.args[0]["message"])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["GET"])
    @cherrypy.tools.json_out()
    def find_shared_files_by_lab(self, signature):
        try:
            laboratory = self.user_service.get_user_from_token(
                signature, os.getenv("MESSAGE")
            )
            shared_list = self.shared_service.find_shared_files_by_lab(laboratory)
            genotype_list = self.genotype_service.shared_list_to_genotype_list(
                shared_list
            )
            return genotype_list
        except Exception as e:
            msg = ""
            if "message" in e.args[0]:
                msg = str(e.args[0]["message"])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["POST"])
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def verify_dataset_status(self):
        try:
            biosample_data = cherrypy.request.json
            user_signature = biosample_data["signature"]
            biosample_id = biosample_data["biosampleId"]
            permittee_serial = biosample_data["permitteeSertial"]
            user_wallet = self.user_service.get_user_from_token(
                user_signature, os.getenv("MESSAGE")
            )
            biosample_db = self.biosample_service.find_biosample_by_serial_or_die(
                biosample_id
            )
            self.biosample_service.verify_biosample_ownership_or_die(
                biosample_db, user_wallet
            )
            filename = self.bucket_service.get_file_name(biosample_id, permittee_serial)
            return {"filename": filename}
        except Exception as e:
            msg = ""
            if "message" in e.args[0]:
                msg = str(e.args[0]["message"])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["POST"])
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def get_permitte_tree_bucket(self):
        try:
            permittee_metadata = cherrypy.request.json
            permittee_signature = permittee_metadata["permitteeSignature"]
            user_wallet = self.user_service.get_user_from_token(
                permittee_signature, os.getenv("MESSAGE")
            )
            files = self.bucket_service.get_file_routes(
                user_wallet, permittee_metadata["route"]
            )
            return {"files": files}
        except Exception as e:
            msg = ""
            if "message" in e.args[0]:
                msg = str(e.args[0]["message"])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["GET"])
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def open_user_bucket_folder(self, user_sign, folder_path, biosample_serial, source):
        try:
            wallet = self.user_service.get_user_from_token(
                user_sign, os.getenv("MESSAGE")
            )
            if source == "USERDASHBOARD":
                files = self.bucket_service.get_user_file_rutes(wallet, folder_path)
                return {"files": files}
            elif source == "LABDASHBOARD":
                self.permittee_service.is_permittee(wallet)
                lab_serial = self.permittee_service.get_serial_from_address(wallet)
                _filter = {
                    "serial": int(biosample_serial),
                    "permitteeSerial": str(lab_serial),
                }
                biosample_activation = self.biosample_activation_service.fetch(_filter)
                if not biosample_activation:
                    raise Exception("Biosample Activation not found")
                biosample_activation = biosample_activation["data"]
                biosample = self.biosample_service.find_biosample_by_serial_or_die(
                    biosample_activation[0]["serial"]
                )
                if biosample and biosample["status"] == "ACTIVE":
                    files = self.bucket_service.get_user_file_rutes(
                        biosample["owner"].upper(), folder_path
                    )
                    return {"files": files}
                else:
                    raise Exception("Biosample not shared")
            else:
                raise Exception("Invalid Source")
        except Exception as e:
            msg = ""
            if "message" in e.args[0]:
                msg = str(e.args[0]["message"])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["POST"])
    @cherrypy.tools.json_out()
    def upload_to_user_bucket(
        self,
        user_sign,
        biosample_serial,
        destination_path,
        source,
        file=None,
        source_path_list=None,
        method=None,
    ):
        try:
            allowed_sources = ["USERDASHBOARD", "LABDASHBOARD"]
            if source.upper() not in allowed_sources:
                raise Exception(f"Invalid Source: allowed: {allowed_sources}")
            wallet_caller = self.user_service.get_user_from_token(
                user_sign, os.getenv("MESSAGE")
            )
            if source == "USERDASHBOARD":
                return self._upload_from_user_dashboard(
                    wallet_caller, biosample_serial, destination_path, file
                )
            if source == "LABDASHBOARD":
                return self._upload_from_lab_dashboard(
                    wallet_caller,
                    biosample_serial,
                    destination_path,
                    method,
                    source_path_list,
                    file,
                )
        except Exception as e:
            msg = ""
            if 'message' in e.args[0]:
                msg = str(e.args[0]['message'])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)

    def _upload_from_user_dashboard(
        self, wallet_caller, biosample_serial, destination_path, file
    ):
        static_path = os.getenv("BUCKET_PATH") + "/users/"
        if file is None:
            raise Exception("file is required")
        biosample = self.biosample_service.find_biosample_by_serial_or_die(
            biosample_serial
        )
        if not biosample or not biosample["owner"].upper() == wallet_caller.upper():
            raise Exception(
                f"You are not the owner of the Biosample: {biosample_serial}"
            )
        full_destination_path = (
            static_path
            + wallet_caller.upper()
            + "/"
            + str(biosample_serial)
            + destination_path
        )
        biosample_activation = self.biosample_activation_service.find_by_serial(
            biosample_serial
        )
        if not biosample_activation:
            raise Exception("Biosample Activation not found")
        permittee = self.permittee_service.find_by_serial(
            int(biosample_activation["permitteeSerial"])
        )

        biosample_metadata = {
            "biosample_serial": int(biosample_serial),
            "owner": biosample["owner"],
            "permittee_serial": permittee["serial"],
            "user_wallet": wallet_caller,
        }

        uploaded = self.bucket_service.upload_file_to_bucket(
            file,
            full_destination_path,
            os.getenv("BUCKET_ACCESS_KEY_ID"),
            os.getenv("BUCKET_SECRET_ACCESS_KEY_ID"),
            os.getenv("BUCKET_NAME"),
        )
        self.notarize_delivery(biosample_metadata, wallet_caller)

        return {"uploaded": uploaded}

    def _upload_from_lab_dashboard(
        self,
        wallet_caller,
        biosample_serial,
        destination_path,
        method,
        source_path_list,
        file,
    ):
        allowed_methods = ["BUCKET", "LOCAL"]
        if method is None:
            raise Exception("method is required")
        if method.upper() not in allowed_methods:
            raise Exception(f"method not supported; allowed: {allowed_methods}")
        self.permittee_service.is_permittee(wallet_caller)
        lab_serial = self.permittee_service.get_serial_from_address(wallet_caller)
        _filter = {"serial": int(biosample_serial), "permitteeSerial": str(lab_serial)}
        biosample_activation = self.biosample_activation_service.fetch(_filter)
        if not biosample_activation:
            raise Exception("Biosample Activation not found")
        biosample_activation = biosample_activation["data"]
        biosample = self.biosample_service.find_biosample_by_serial_or_die(
            biosample_activation[0]["serial"]
        )
        if not biosample or not biosample["status"] == "ACTIVE":
            raise Exception("Biosample not shared")
        static_path = os.getenv("BUCKET_PATH") + "/users/"
        full_destination_path = (
            static_path
            + biosample["owner"].upper()
            + "/"
            + str(biosample_serial)
            + destination_path
        )

        biosample_metadata = {
            "biosample_serial": int(biosample_serial),
            "owner": biosample["owner"],
            "permittee_serial": lab_serial,
            "user_wallet": wallet_caller,
        }

        if method.upper() == "BUCKET":
            if source_path_list is None:
                raise Exception("source_path is required")
            source_path_list = ast.literal_eval(source_path_list)
            #  METHOD TO TRANSFER BUCKET TO BUYCKET

            self.bucket_service.transfer_permittee_bucket_to_bucket(
                source_path_list,
                lab_serial,
                os.getenv("BUCKET_ACCESS_KEY_ID"),
                os.getenv("BUCKET_SECRET_ACCESS_KEY_ID"),
                os.getenv("BUCKET_NAME"),
                full_destination_path,
            )
            biosample_metadata["file_routes"] = {
                path.split("/")[-1]: path for path in source_path_list
            }
            self.notarize_delivery(biosample_metadata, wallet_caller)

            return {"uploaded": "UPLOAD USING BUKET TO BUCKET"}
        if method.upper() == "LOCAL":
            if file is None:
                raise Exception("file is required")
            uploaded = self.bucket_service.upload_file_to_bucket(
                file,
                full_destination_path,
                os.getenv("BUCKET_ACCESS_KEY_ID"),
                os.getenv("BUCKET_SECRET_ACCESS_KEY_ID"),
                os.getenv("BUCKET_NAME"),
            )
            biosample_metadata["file_routes"] = {file.filename: file.filename}
            self.notarize_delivery(biosample_metadata, wallet_caller)

            return {"uploaded": uploaded}

    def notarize_delivery(self, biosample_metadada, permittee_wallet):
        biosample_metadada["delivery_tx"] = self.delivery_service.notarize(
            biosample_metadada, permittee_wallet
        )
        biosample_metadada["type"] = "TRANSFER"
        self.delivery_service.create_or_die(biosample_metadada)
        self.biosample_service.set_delivered_biosample(
            biosample_metadada["biosample_serial"],
            True,
            biosample_metadada["delivery_tx"],
        )

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["GET"])
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def download_user_file_from_bucket(self, user_sign, path_list):
        path_list = path_list.split("|")
        try:
            user_wallet = self.user_service.get_user_from_token(
                user_sign, os.getenv("MESSAGE")
            )
            link = self.bucket_service.get_user_bucket_file_link(
                user=user_wallet.upper(), path_list=path_list, expiration=1
            )
            return {"link": link}
        except Exception as e:
            msg = ""
            if "message" in e.args[0]:
                msg = str(e.args[0]["message"])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["GET"])
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def download_user_file_from_bucket_from_labdashboard(
        self, user_sign, path_list, biosample_serial
    ):
        path_list = path_list.split("|")
        try:
            user_wallet = self.user_service.get_user_from_token(
                user_sign, os.getenv("MESSAGE")
            )
            self.permittee_service.is_permittee(user_wallet)
            lab_serial = self.permittee_service.get_serial_from_address(user_wallet)
            _filter = {
                "serial": int(biosample_serial),
                "permitteeSerial": str(lab_serial),
            }
            biosample_activation = self.biosample_activation_service.fetch(_filter)
            if not biosample_activation:
                raise Exception("Biosample Activation not found")
            biosample_activation = biosample_activation["data"]
            biosample = self.biosample_service.find_biosample_by_serial_or_die(
                biosample_activation[0]["serial"]
            )
            if not biosample or not biosample["status"] == "ACTIVE":
                raise Exception("Biosample not shared")
            link = self.bucket_service.get_user_bucket_file_link(
                user=biosample["owner"].upper(),
                path_list=path_list,
                downloadable=False,
                expiration=11400,
            )
            return {"link": link}
        except Exception as e:
            msg = ""
            if "message" in e.args[0]:
                msg = str(e.args[0]["message"])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["GET"])
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def get_my_uploaded_files_urls(self, user_signature):
        try:
            self.logger.info("GET/get_my_uploaded_files_urls/  user_signature: %s", user_signature)
            user_wallet = self.user_service.get_user_from_token(
                user_signature, os.getenv("MESSAGE")
            )
            print("\n\n Userwallet: ", user_wallet)
            self.logger.debug("User wallet fetched: %s", user_wallet)
            excluded_extensions = [".gz"]
            genotype_list = self.genotype_service.fetch(
                {
                    "owneraddr": str(user_wallet).upper(),
                }
            )
            file_list = []
            for genotype in genotype_list:
                genotype_extension = "." + genotype.get("extension", "").lower()
                if genotype_extension in excluded_extensions:
                    continue
                file = {
                    "filename": genotype["filename"],
                    "path": genotype["filename"],
                    "type": "UPLOADED",
                    "original_name": genotype.get(
                        "original_filename",
                        genotype.get("filename", "")
                        + "."
                        + genotype.get("extension", ""),
                    ),
                    "extension": genotype.get("extension", ""),
                }
                file_list.append(file)
            biosamples = self.biosample_service.fetch({"owner": user_wallet})
            for biosample in biosamples["data"]:
                bucket_files = self.bucket_service.get_user_file_rutes(
                    biosample["owner"].upper(), str(biosample["serial"]) + "/"
                )
                if not bucket_files:
                    continue
                for bucket_file in bucket_files:
                    if bucket_file.endswith("/"):
                        continue
                    filename = os.path.basename(bucket_file)
                    _, file_extension = os.path.splitext(bucket_file)
                    if file_extension.lower() in excluded_extensions:
                        continue
                    path = "/".join(bucket_file.split("/")[1:])
                    file = {
                        "filename": filename,
                        "path": path,
                        "biosample_serial": biosample["serial"],
                        "owner": biosample["owner"],
                        "type": "TRANSFER",
                        "original_name": filename,
                        "extension": file_extension,
                    }
                    file_list.append(file)
            return file_list
        except Exception as e:
            msg = ""
            if "message" in e.args[0]:
                msg = str(e.args[0]["message"])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)


    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["GET"])
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def delete_user_file_from_bucket(self, user_sign, path_list):
        path_list = path_list.split("|")
        try:
            user_wallet = self.user_service.get_user_from_token(
                user_sign, os.getenv("MESSAGE")
            )
            deleted = self.bucket_service.delete_user_file_path(
                user=user_wallet.upper(),
                path_list=path_list,
            )

            return {"deleted": deleted}
        except Exception as e:
            msg = ""
            if "message" in e.args[0]:
                msg = str(e.args[0]["message"])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)



    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["POST"])
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def delivery_biosample(self):
        try:
            biosample_metadada = cherrypy.request.json
            user_wallet = self.user_service.get_user_from_token(
                biosample_metadada["user_signature"], os.getenv("MESSAGE")
            )
            biosample_metadada["user_wallet"] = user_wallet
            # create a function to make the notarized transactin by a smartcontract
            biosample_metadada["delivery_tx"] = self.delivery_service.notarize(
                biosample_metadada, user_wallet
            )
            biosample_metadada["type"] = "DELIVERY"
            # copiar los archivos del bucket 'A' al bucketr 'B'
            self.bucket_service.delivery_file_transfer(
                biosample_metadada["biosample_serial"],
                user_wallet,
                biosample_metadada["file_routes"],
            )
            self.delivery_service.create_or_die(biosample_metadada)
            self.biosample_service.set_delivered_biosample(
                biosample_metadada["biosample_serial"],
                True,
                biosample_metadada["delivery_tx"],
            )
            return {"delivery_tx": biosample_metadada["delivery_tx"]}
        except Exception as e:
            msg = ""
            if "message" in e.args[0]:
                msg = str(e.args[0]["message"])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["GET"])
    @cherrypy.tools.json_out()
    def received_biosample_files(self, signature):
        try:
            user = self.user_service.get_user_from_token(
                signature, os.getenv("MESSAGE")
            )
            deliveries =  self.delivery_service.find_all_by_owner_address(user)
            for delivery in deliveries["data"]:
                permittee_profile = self.profile_service.fetch_one({"serial": int(delivery.get("permittee_id", 0))})
                delivery["permittee_profile"] = permittee_profile
            return deliveries

        except Exception as e:
            msg = ""
            if "message" in e.args[0]:
                msg = str(e.args[0]["message"])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.json_out()
    def download_received_biosample_file(self, signature, serial):
        try:
            owner = self.user_service.get_user_from_token(
                signature, os.getenv("MESSAGE")
            )
            self.delivery_service.is_owner_or_die(serial, owner)
            # delivery = self.delivery_service.find_by_biosample_serial(serial)

            delivery_files = self.delivery_service.find_by_biosample_serial(int(serial))
            if not delivery_files:
                raise Exception(f"Files Not found")
            delivery_files = delivery_files["data"]
            file_paths = [
                {"path": value, "type": delivery["type"], "owner": delivery["owner"]}
                for delivery in delivery_files
                for value in (
                    delivery["files"].values()
                    if isinstance(delivery["files"], dict)
                    else delivery["files"]
                )
            ]
            local_bucket_paths = []
            for path in file_paths:
                if path["type"] == "TRANSFER":
                    bucket_route = f"{os.getenv('BUCKET_PATH')}/users/{path['owner'].upper()}/{serial}/{path['path']}"
                    local_bucket_paths.append(bucket_route)
                elif path["type"] == "DELIVERY":
                    external_file_path = path["path"][2:]
                    file_name = os.path.basename(external_file_path)
                    bucket_route = (
                        f"{os.getenv('BUCKET_PATH')}/deliveries/{serial}/{file_name}"
                    )
                    local_bucket_paths.append(bucket_route)

            print("\n\n\n LOCAL BUKETS PATH: ", local_bucket_paths)
            link = self.bucket_service.get_presigned_link(
                path_list=local_bucket_paths, expiration=5
            )
            return {"link": link}
        except Exception as e:
            msg = ""
            if "message" in e.args[0]:
                msg = str(e.args[0]["message"])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["GET"])
    @cherrypy.tools.json_out()
    def deliveries(self, permittee_id=None):
        try:
            if not permittee_id:
                return self.delivery_service.find_all()
            else:
                return self.delivery_service.find_by_permittee_serial(permittee_id)
        except Exception as e:
            msg = ""
            if "message" in e.args[0]:
                msg = str(e.args[0]["message"])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["POST"])
    @cherrypy.tools.json_out()
    def create_magic_link(self, signature, data):
        try:
            data = json.loads(data)
            permittee = self.user_service.get_user_from_token(
                signature, os.getenv("MESSAGE")
            )
            print("\n\n\n data: ", data)
            self.permittee_service.is_permittee(permittee)
            permittee_id = self.permittee_service.get_serial_from_address(permittee)
            data["permittee"] = permittee
            data["permittee_id"] = permittee_id
            self.biosample_activation_service.create(data)
            activation_url = self.magic_link_service.create(data)
            return {"magic_link": activation_url}
        except Exception as e:
            msg = ""
            if "message" in e.args[0]:
                msg = str(e.args[0]["message"])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)
    

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["GET"])
    @cherrypy.tools.json_out()
    def find_magic_links(self, creator_signature):
        try:
            permittee = self.user_service.get_user_from_token(
                creator_signature, os.getenv("MESSAGE")
            )
            self.permittee_service.is_permittee(permittee)
            permittee_serial = self.permittee_service.get_serial_from_address(permittee)
            magic_links = self.magic_link_service.find_by_creator_serial(
                permittee_serial
            )
            for magic_link in magic_links["data"]:
                biosample = self.biosample_service.fetch_one(
                    {"serial": int(magic_link["biosample_id"])}
                )
                magic_link["isActive"] = biosample != []
            return magic_links
        except Exception as e:
            msg = ""
            if "message" in e.args[0]:
                msg = str(e.args[0]["message"])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)

    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["POST"])
    @cherrypy.tools.json_out()
    def delete_magic_link(self, creator_signature, link):
        try:
            print("\n\n\n creator_signature:", creator_signature)
            print("\n\n\n link:", link)
            permittee = self.user_service.get_user_from_token(
                creator_signature, os.getenv("MESSAGE")
            )
            self.permittee_service.is_permittee(permittee)
            permittee_serial = self.permittee_service.get_serial_from_address(permittee)
            magic_link = self.magic_link_service.fetch_one(
                {"creator_id": int(permittee_serial), "link": link}
            )
            if not magic_link:
                raise cherrypy.HTTPError(
                    "500 Internal Server Error", "User is not creator"
                )
            biosample = self.biosample_service.fetch_one(
                {"serial": int(magic_link["biosample_id"])}
            )
            if biosample:
                raise cherrypy.HTTPError(
                    "500 Internal Server Error",
                    "It cannot be deleted because the biosample is already activated",
                )
            self.magic_link_service.delete_link(
                {"creator_id": int(permittee_serial), "link": link}
            )
        except Exception as e:
            msg = ""
            if 'message' in e.args[0]:
                msg = str(e.args[0]['message'])
            else:
                msg = str(e)
            raise cherrypy.HTTPError("500 Internal Server Error", msg)


    @cherrypy.expose
    @cherrypy.config(**{"tools.CORS.on": True})
    @cherrypy.tools.allow(methods=["GET"])
    @cherrypy.tools.json_out()
    def get_user_balance(self, user_address):
        user_balance = self.user_service.get_balance(user_address)
        return user_balance


class AppServerManager(object):
    def __init__(self) -> None:
        return None

    def start(self, port):
        server = Server()

        CONF = {
            "/static": {
                "tools.staticdir.on": True,
                "tools.staticdir.dir": abspath("./public"),
                "tools.CORS.on": True,
            },
            "/js": {
                "tools.staticdir.on": True,
                "tools.staticdir.dir": abspath("./public/pages/js"),
            },
            "/images": {
                "tools.staticdir.on": True,
                "tools.staticdir.dir": abspath("./public/images"),
            },
            "/": {
                "tools.sessions.on": True,
                "tools.response_headers.on": True,
                "tools.CORS.on": True,
                "tools.sessions.timeout": 60 * 60 * 24 * 365,
            }
        }
        cherrypy.server.socket_host = "0.0.0.0"
        cherrypy.server.socket_port = port
        cherrypy.server.socket_timeout = 60 * 60 * 24 * 365
        cherrypy.server.max_request_body_size = 0
        cherrypy.quickstart(server, "/", CONF)
