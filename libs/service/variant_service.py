import os

from libs.dao import variant_dao
from libs.exceptions import DomainInjectionError


class variantService:
    def __init__(self, _variant_dao):
        if not isinstance(_variant_dao, variant_dao.VariantDAO):
            raise DomainInjectionError.DomainInjectionError(
                "magic_link_service", "magic_link"
            )
        self.variant_dao = _variant_dao

    def create(self, data):
        return self.variant_dao.create(data)

    def fetch(self, _filter):
        result = self.variant_dao.fetch(_filter)
        if not result:
            return []
        return result

    def fetch_one(self, _filter):
        result = self.variant_dao.fetch(_filter)
        if not result:
            return []
        return result[0]

    def update(self, _filter, new_data):
        self.variant_dao.update(_filter, new_data)

    def delete_one(self, _filter):
        deleted = self.variant_dao.delete(_filter)
        return deleted
