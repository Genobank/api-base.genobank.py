import json
from datetime import datetime

class json_helper_dao:
    def __init__(self):
        return None
    
    def serialize_cur (self, cur):
        row = []
        for doc in cur:
            row.append(self.serialize_doc(doc))
        return row
  
    def serialize_doc(self, doc):
        if not doc:
            return []
        else:
            for key in doc:
                if isinstance(doc[key], list):
                    doc[key] = self.serialize_cur(doc[key])
                else:
                    if (not isinstance(doc[key], str)) and (not isinstance(doc[key], int)) and (not isinstance(doc[key], float)) and (not isinstance(doc[key], dict)):
                        doc[key] = str(doc[key])
            return doc


