from libs.dao import contract_dao
from libs.exceptions import DomainInjectionError


class ContractService:
    def __init__(self, _contract):
        if not isinstance(_contract, contract_dao.ContractDAO):
            raise DomainInjectionError.DomainInjectionError(
                "contract_service", "contract"
            )
        self.contract_dao = _contract

    def deploy(self, name, symbol, lab_address):
        deployed_contract = self.contract_dao.deploy(name, symbol, lab_address)
        return deployed_contract

    def deploy_or_fail(self, metadata):
        deployed_contract = self.contract_dao.deploy(metadata)
        if not deployed_contract:
            raise Exception("Error creating token manager")
        return deployed_contract

    def store_deployment_record(self, metadata):
        inserted = self.contract_dao.store_deployment_record(metadata)
        return inserted

    def fetch(self, filter={}):
        contract = self.contract_dao.fetch(filter)
        return contract

    def fetch_one(self, filter={}):
        contract = self.contract_dao.fetch(filter)
        if not contract:
            return []
        return contract[0]
