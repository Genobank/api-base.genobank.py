from libs.dao import xBPT_dao
from libs.exceptions import DomainInjectionError

class xBPT_service:
    def __init__(self, _XBPT,):
        if not isinstance(_XBPT, xBPT_dao.XBPT_DAO):
            raise DomainInjectionError.DomainInjectionError("email_service", "email")		
        self.XBPT_dao = _XBPT

    def notarize(self, action_type, metadata):
        notarized_tx_hash = self.XBPT_dao.notarize_event(action_type, metadata)
        return notarized_tx_hash
        
    def get_event_by_index(self, _index):
        return self.XBPT_dao.get_event_by_index(_index)
    
    def get_all_events(self):
        return self.XBPT_dao.get_all_events()
    
