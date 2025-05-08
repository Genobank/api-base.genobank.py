import os

from libs.dao import magic_link_dao
from libs.exceptions import DomainInjectionError


class magic_link_service:
    def __init__(
        self,
        _magic_link,
    ):
        if not isinstance(_magic_link, magic_link_dao.magic_link_dao):
            raise DomainInjectionError.DomainInjectionError(
                "magic_link_service", "magic_link"
            )
        self.magic_link = _magic_link

    def create(self, data):
        secret = self.magic_link.create_biosample_hmac(int(data["biosampleId"]))
        url = self.magic_link.create_activation_url(
            data["domain"] + "/activate",
            int(data["biosampleId"]),
            data["permittee_id"],
            data["physicalId"],
            secret,
        )
        self.magic_link.save_db(data, url)
        return url

    def find_all(self):
        return self.magic_link.find_all()

    def fetch(self, _filters={}):
        magic_urls = self.magic_link.fetch(_filters)
        if not magic_urls:
            return []
        else:
            return magic_urls

    def fetch_one(self, _filters={}):
        magic_urls = self.magic_link.fetch(_filters)
        if not magic_urls:
            return []
        return magic_urls[0]

    def find_by_creator_wallet(self, wallet):
        return self.magic_link.find_by_creator_wallet(wallet)

    def find_by_creator_serial(self, serial):
        magic_urls = self.magic_link.find_by_creator_serial(serial)
        print("\n\n\n magic_urls", magic_urls)

        return {"data": magic_urls}

    def is_link_creator(self, creator_walet, link):
        is_creator = self.magic_link.is_link_creator(creator_walet, link)
        return is_creator

    def delete_link(self, _query):
        deleted = self.magic_link.delete(_query)
        return deleted
