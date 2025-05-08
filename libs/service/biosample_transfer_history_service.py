import os
from decimal import Decimal

from libs.dao import biosample_transfer_history_dao


class BiosampleTransferHistoryService:
    def __init__(self):
        self.biosample_transfer_history = biosample_transfer_history_dao.BiosampleTransferHistoryDAO()

    def create(self, data):
        return self.biosample_transfer_history.create(data)

    def fetch(self, _filter={}, projection=None, exclude=True, skip=0, limit=0, sort=[("createdAt", -1)], **kwargs):
        registration = self.biosample_transfer_history.fetch(
            _filter=_filter,
            projection=projection,
            exclude=exclude,
            skip=skip,
            limit=limit,
            sort=sort,
            **kwargs)
        if not registration:
            return []
        return registration

    def fetch_one(self, _filter={}, projection=None, exclude=True, skip=0, sort=[("createdAt", -1)], **kwargs):
        registration = self.biosample_transfer_history.fetch(
            _filter=_filter,
            projection=projection,
            exclude=exclude,
            skip=skip,
            limit=1,
            sort=sort,
            **kwargs
        )
        if not registration:
            return {}
        return registration[0]

    def update(self, _filter, new_data):
        return self.biosample_transfer_history.update(_filter, new_data)

    def delete_one(self, _filter):
        deleted = self.biosample_transfer_history.delete(_filter)
        return deleted
