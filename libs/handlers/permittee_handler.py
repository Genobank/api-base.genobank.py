import cherrypy
from libs.utils.DefaultHandler import DefaultHandler
from libs.dao import permitte_dao
from libs.service import permittee_service

class PermitteeHandler(DefaultHandler):
    def __init__(self):
        permitte = permitte_dao.permittee_dao()
        self.permittee_service = permittee_service.permittee_service(permitte)
        
    # Check why is not returni the full JSON
    @cherrypy.tools.json_out()
    def get(self, serial=None):
        print(f"\n\n\n serial: {serial}")
        if not serial:
            print(f"\n\n\n data: {self.permittee_service.find_all()}")
            return {"data":self.permittee_service.find_all()}
        else:
            return self.permittee_service.find_by_serial(serial)
        
    def post(self, *args, **kwargs):
        return "Sample Of post method"
    
    def delete(self):
        return "sample of Delete"
    
    def put(self):
        return "sample of put"
    
    def patch(self):
        return "sample of patch"
