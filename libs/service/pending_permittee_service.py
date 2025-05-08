from libs.dao import pending_permittee_dao as dao
from libs.exceptions import DomainInjectionError

class pending_permittee_service:
    def __init__(self, pending_permittee):
        if not isinstance(pending_permittee, dao.pending_permittee_dao):
            raise DomainInjectionError.DomainInjectionError("pending_permittee_service", "pending_permittee")
        self.pending_permittee = pending_permittee


    def create(self, all_data):
        pending_permittee = bool(self.pending_permittee.find_by_owner(all_data["Owner"]))
        if pending_permittee:
            raise Exception("Permittee "+str(all_data["Owner"])+" is already waiting to be approved")
        return self.pending_permittee.create(all_data)

    def find_all_pending_permittee(self):
        all_pending_permittees = self.pending_permittee.find_all_pendig_permittees()
        refactored = []
        for pending in all_pending_permittees:
            refactored.append(self.jsonify(pending))
        return refactored
    

    
    def reject_pending_permittee_status(self, owner):
        self.pending_permittee.change_pending_permittee_status(owner, 2)


    def add_pendig_serial(self, owner, serial):
        return self.pending_permittee.add_pendig_serial(owner, serial)

    def change_status(self, owner, status):
        return self.pending_permittee.change_pending_permittee_status(owner, status)
    
    def find_by_owner(self, owner):
        return self.pending_permittee.find_by_owner(owner)
    
    def approve_permittee(self, data):
        return self.pending_permittee.approve_permittee(data)
    

    def jsonify(self, pending_permittees):
        if "_id" in pending_permittees: del pending_permittees["_id"]
        return pending_permittees
    
