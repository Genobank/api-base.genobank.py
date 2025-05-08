import ast
import json

from libs.dao import profile_dao
from libs.exceptions import DomainInjectionError


class profile_service:
    def __init__(self, profile):
        if not isinstance(profile, profile_dao.profile_dao):
            raise DomainInjectionError.DomainInjectionError(
                "profile_service", "profile"
            )
        self.profile = profile

    def create(self, profile_metadata):
        self.validate_profile_schema_or_die(profile_metadata)
        self.profile.create(profile_metadata)

    def validate_profile_schema_or_die(self, profile):
        if "serial" not in profile:
            raise Exception("Error serial not in profile")
        if "text" not in profile:
            raise Exception("Error text not in profile")

    def find_all(self):
        return self.profile.find_all()

    def find_by_serial(self, serial):
        profile = self.profile.find_by_serial(serial)
        if not profile:
            raise Exception("400 Profile Not Found")
        return profile

    def get_permittee_name(self, serial):
        profile = self.profile.find_by_serial(serial)
        if not profile:
            return ""
        profile_text = json.loads(profile["data"]["text"])
        name = profile_text.get("name", "")
        return name

    def get_permittee_email(self, serial):
        profile = self.profile.find_by_serial(serial)
        if not profile:
            return ""
        profile_text = json.loads(profile["data"]["text"])
        name = profile_text.get("email", "")
        return name

    def fetch(self, _filter, projection={}, exclude=True):
        result = self.profile.fetch(_filter, projection, exclude)
        if not result:
            return []
        return result

    def fetch_one(self, _filter, projection={}, exclude=True):
        result = self.profile.fetch(_filter, projection, exclude)
        if not result:
            return []
        return result[0]
