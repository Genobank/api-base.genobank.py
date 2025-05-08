from libs.dao import license_dao
from libs.exceptions import DomainInjectionError

class license_service:
	def __init__(self, _licence):
		if not isinstance(_licence, license_dao.license_dao):
			raise DomainInjectionError.DomainInjectionError("licence_service", "licence")
		self.licence = _licence

	def create_licence(self, metadata):
		licence_created = self.licence.create_licence(metadata)
		if not licence_created:
			raise Exception("Error during creation of licence")
		return licence_created

	def find_license_by_permitte_and_type (self, permittee, type):
		licence = self.licence.find_license_by_permitee_and_type(permittee, type)
		if not licence:
			return False
		return licence[0]
		
	def delete_license (self, permittee, type):
		deleted = self.licence.delete_license(permittee, type)
		if not deleted:
			raise Exception("Error during deleting licence")
		return deleted