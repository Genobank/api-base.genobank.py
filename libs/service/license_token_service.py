from libs.dao import license_token_dao


class LicenseTokenService:
    def __init__(self):
        self.license_token_dao = license_token_dao.LicenseTokenDao()

    def create(self, data):
        created = self.license_token_dao.create(data)
        return created

    def fetch(self, _filter):
        result = self.license_token_dao.fetch(_filter)
        if not result:
            return []
        return result
    
    def fetch_one(self, _filter):
        result = self.license_token_dao.fetch(_filter)
        if not result:
            return {}
        return result[0]