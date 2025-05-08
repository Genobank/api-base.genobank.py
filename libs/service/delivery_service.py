from libs.dao import delivery_dao
from libs.exceptions import DomainInjectionError


class delivery_service:
    def __init__(self, _delivery,):
        if not isinstance(_delivery, delivery_dao.delivery_dao):
            raise DomainInjectionError.DomainInjectionError("delivery_service", "delivery")		
        self.delivery = _delivery
        
    def create_or_die(self, delivery_json):
        created =  self.delivery.create(delivery_json)
        if not created:
            raise Exception("Error creating delivery")
    
    def find_all(self):
        deliveries = self.delivery.find_all()
        if not deliveries:
            return []
        return self.delivery.cur_list_to_scheme(deliveries)
    
    def is_owner_or_die(self, serial, owner):
        is_owner = self.delivery.find_by_biosample_serial_and_owner(serial, owner)
        print("is_owner", is_owner)
        if not is_owner:
            raise Exception("This user is not allowed to access this file")
        return is_owner
    
    def find_by_permittee_serial(self, permittee_serial):
        deliveries = self.delivery.find_by_permittee_serial(permittee_serial)
        if not deliveries:
            return []
        return self.delivery.cur_list_to_scheme(deliveries)
    
    def find_by_biosample_serial(self, biosample_serial):
        deliveries = self.delivery.find_by_biosample_serial(biosample_serial)
        if not deliveries:
            return []
        return self.delivery.cur_list_to_scheme(deliveries)
    
    def find_all_by_owner_address(self, owner_address):
        deliveries = self.delivery.find_by_owner_address(owner_address)
        print("debug deliveries: ", deliveries)
        if not deliveries:
            return []
        return self.delivery.cur_list_to_scheme(deliveries)
    
    def notarize(self, metadata, wallet):
        serial = metadata["biosample_serial"]
        owner = metadata["owner"]
        lab = wallet

        return self.delivery.notarize(serial, owner, lab)


    def fetch(self, _filter={}, projection=None, exclude=True, skip=0, limit=0, sort=[("created", -1)], **kwargs):
        registration = self.delivery.fetch(
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

    def fetch_one(self, _filter={}, projection=None, exclude=True, skip=0, sort=[("created", -1)], **kwargs):
        registration = self.delivery.fetch(
            _filter=_filter,
            projection=projection,
            exclude=exclude,
            skip=skip,
            limit=1,  # Establecemos limit=1 para obtener un solo registro
            sort=sort,
            **kwargs
        )
        if not registration:
            return {}
        return registration[0]

