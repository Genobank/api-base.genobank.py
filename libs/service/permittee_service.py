from curses import meta
from math import perm
from re import S
from urllib import response
from libs.dao import permitte_dao as dao
from libs.exceptions import DomainInjectionError
from dotenv import load_dotenv
import requests
import os
class permittee_service:
    def __init__(self, permittee):
        if not isinstance(permittee, dao.permittee_dao):
            raise DomainInjectionError.DomainInjectionError("permittee_service", "permittee")
        self.permittee = permittee

    def create_permittee(self, id, address, secret):
        try:
            is_registered  = self.permittee.find_by_serial(int(id))
            if is_registered:
                return False, "Permittee ID #" + id + " was already registered."
            else:
                created = self.permittee.create_permittee(id, address, secret)
                if not created:
                    raise Exception("Failed to create new permittee, please try again later")
                return created
        except:
            raise

    def check_sum_address(self, address):
        return self.permittee.check_sum_address(address)

    def find_all_permittees (self):
        permittees_list = self.permittee.find_all_permittees()
        return permittees_list

    def get_serial_from_address(self, address):
            serial = self.permittee.get_serial_from_address(address)
            if not serial:
                return[]
            return serial

    def find_by_owner(self, owner):
        return self.permittee.find_by_owner(owner)

    def validate_permittee(self, permittee):
            validated = self.permittee.validate_permittee(permittee)
            if not validated:
                return False
            return validated

    def validate_permittee_signature(self, metadata):
            permittee = metadata["lab_address"]
            msg = metadata["msg"]
            signature = metadata["signature"]
            validated = self.permittee.validate_permittee_signature(
                permittee,
                msg,
                signature
            )
            if not validated:
                raise Exception("Failed to validate permittee signature")
            return validated

    def basic_reference(self, _permittee):
        if not _permittee:
            return False
        _json = {}
        _json["public_address"] = _permittee["owner"]
        _json["id_number"] = _permittee["serial"]
        _json["status"] = _permittee["status"]
        return _json
        
    def is_permittee(self, address):
        permittee = self.permittee.validate_permittee(address)
        if not address:
            raise Exception("Address is no permittee")
        return permittee

    def is_valid_permittee(self, permittee_serial:int):
        permittee_serial = self.permittee.find_by_serial(permittee_serial)
        return permittee_serial
        
    def get_next_enabled_serial(self):
        return self.permittee.get_next_enabled_serial()
    
    def find_all(self):
        return self.permittee.find_all()
    
    def find_by_serial(self, serial):
        profile = self.permittee.find_by_serial(serial)
        if not profile:
            raise ValueError("400 Permittee Not Found")
        return profile
