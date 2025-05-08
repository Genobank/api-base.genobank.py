from libs.utils.DefaultHandler import DefaultHandler
class ExampleHandler(DefaultHandler):
    def get(self, *args, **kwargs):
        return "GET METHOD"
        
    def post(self, *args, **kwargs):
        return "Sample Of post method"
    
    def delete(self):
        return "sample of Delete"
    
    def put(self):
        return "sample of put"
    
    def patch(self):
        return "sample of patch"
