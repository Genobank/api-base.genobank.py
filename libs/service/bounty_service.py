import os
from decimal import Decimal

from bson.decimal128 import Decimal128

from libs.dao import bounty_dao
from libs.exceptions import DomainInjectionError


class bountyService:
    def __init__(self, _bounty_dao):
        if not isinstance(_bounty_dao, bounty_dao.BountyDAO):
            raise DomainInjectionError.DomainInjectionError(
                "magic_link_service", "magic_link"
            )
        self.bounty_dao = _bounty_dao

    def create(self, data):
        amount = Decimal(data["amount"])
        print("\n\n\n amount: ", amount)
        exist = self.fetch_one({"biosample_serial": int(data["biosampleSerial"])})
        if not exist:
            comission = Decimal(amount / 10)
            net_amount = Decimal(amount - comission)
            print("\n\n\n comission: ", comission)
            print("\n\n\n net_amount: ", net_amount)

            data["comission"] = comission
            data["net_amount"] = net_amount
            return self.bounty_dao.create(data)
        existing_amount = Decimal(exist["totalamount"])
        update_amount = existing_amount + amount
        update_comission = Decimal(update_amount / 10)
        update_net_amount = update_amount - update_comission
        _filter = {"biosample_serial": int(data["biosampleSerial"])}
        return self.update(
            _filter,
            {
                "totalamount": float(update_amount),
                "net_amount": float(update_net_amount),
                "comission": float(update_comission),
            },
        )

    def fetch(self, _filter):
        result = self.bounty_dao.fetch(_filter)
        if not result:
            return []
        return result

    def fetch_one(self, _filter):
        result = self.bounty_dao.fetch(_filter)
        if not result:
            return []
        return result[0]

    def update(self, _filter, new_data):
        return self.bounty_dao.update(_filter, new_data)

    def delete_one(self, _filter):
        deleted = self.bounty_dao.delete(_filter)
        return deleted
