from libs.dao import nft_dao
from libs.exceptions import DomainInjectionError


class NFTService:
    def __init__(self, _nft):
        if not isinstance(_nft, nft_dao.NFTDAO):
            raise DomainInjectionError.DomainInjectionError("nft_service", "nft")
        self.nft_dao = _nft

    def mint(self, contract_address, to_user, to_lab, metadata={}):
        minted_nft = self.nft_dao.mint(contract_address, to_user, to_lab, metadata)
        return minted_nft

    def mint_or_fail(self, metadata):
        minted_nft = self.nft_dao.mint(metadata)
        if not minted_nft:
            raise ValueError("Error creating token manager")
        return minted_nft

    def get_NFT(self, contract_address, lab_address, user_address):
        nft = self.nft_dao.get_NFT(contract_address, lab_address, user_address)
        return nft

    def store_mint_record(self, metadata):
        inserted = self.nft_dao.store_mint_record(metadata)
        return inserted

    def fetch(self, _filters={}, _projection={}):
        nft_list = self.nft_dao.fetch(_filters, _projection)
        return nft_list

    def fetch_one(self, _filters={}):
        nft = self.nft_dao.fetch(_filters)
        if not nft:
            return []
        return nft[0]
