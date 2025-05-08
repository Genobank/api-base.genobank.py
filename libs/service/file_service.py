# from re import T
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


class FileWrapper:
    def __init__(self, content, filename='data.txt'):
        # Si el contenido es una cadena, usa StringIO, de lo contrario usa BytesIO
        if isinstance(content, str):
            self.file = io.StringIO(content)
        else:
            self.file = io.BytesIO(content)
        self.filename = filename

class FileWrapperV2:
    def __init__(self, content, filename='data.txt'):
        # Si el contenido es una cadena, conviértelo a bytes usando UTF-8
        if isinstance(content, str):
            self.file = io.BytesIO(content.encode('utf-8'))
        else:
            self.file = io.BytesIO(content)
        self.filename = filename

class FileService:
    def __init__(self, _file_dao):
        if not isinstance(_file_dao, file_dao.file_dao):
            raise DomainInjectionError.DomainInjectionError("file_service", "file")
        self.file = _file_dao

    def validate_extension(self, ext):
        if ext != "txt":
            raise Exception("Invalid extension you file needs to be a txt extension")
        return True

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
        file.seek(0)
        lines = file.readlines()
        array_snips = self.file.get_snips(lines)
        exist_file = self.file.exists_snips(array_snips)
        if exist_file:
            raise Exception("This file already exists")
        return array_snips

    def get_snips_from_file_string(self, content_str):
        array_snips = self.file.get_optimized_snips(content_str)
        return array_snips

    def csv_to_json(self, csv_string):
        lines = csv_string.strip().split("\n")
        headers = lines[0].split(",")
        values = lines[1].split(",")
        result = {headers[i]: float(values[i]) for i in range(len(headers))}
        return result

    def validate_snips_from_text(self, text):
        array_snips = self.file.get_optimized_snips(text)
        if array_snips:
            exist_file = self.file.exists_snips_optimized(array_snips)
            if exist_file:
                return False
                # raise Exception('This file already exists')
            return array_snips
        else:
            return False

    def validate_file(self, file):
        f = file.read()
        source = self.file.Manejador(f)
        return source

    def format_file(self, content):
        if isinstance(content, str):
            return io.StringIO(content)
        else:
            return io.BytesIO(content)


# create a function to parse a json to a file to be pinned by ipfs
    def json_to_file(self, json_data):
        return io.BytesIO(json.dumps(json_data).encode())