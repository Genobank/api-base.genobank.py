from libs.dao import download_dao
from libs.exceptions import DomainInjectionError


class DownloadService:
    def __init__(self, _download_dao,):
        if not isinstance(_download_dao, download_dao.DownloadDAO):
            raise DomainInjectionError.DomainInjectionError("request_biosample_service", "request_biosample")		
        self.download_dao = _download_dao

    def create(self, metadata):
        inserted = self.download_dao.create(metadata)
        return inserted
    
    def fetch(self, _filters={}):
        biosamples = self.download_dao.fetch(_filters)
        if not biosamples:
            return []
        return biosamples
    
    def fetch_one(self, _filters={}):
        biosamples = self.download_dao.fetch(_filters)
        if not biosamples:
            return []
        return biosamples[0]
    

    def count_by_biosample(self, biosample_serial):
        return self.download_dao.count_by_biosample(biosample_serial)

    def count_by_biosample_and_downloader(self, biosample_serial, downloader_serial):
        return self.download_dao.count_by_biosample_and_downloader(biosample_serial, downloader_serial)
    
    def count_total_downloads(self):
        return self.download_dao.count_total_downloads()