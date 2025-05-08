import json
from datetime import datetime

class json_helper_dao:
    def __init__(self):
        pass

    def default_serializer(self, obj):
        """Serializa tipos de datos no soportados por default por json.dumps."""
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif hasattr(obj, "__dict__"):
            return obj.__dict__
        else:
            return str(obj)

    def serialize_cur(self, cur):
        """Serializa una colección de documentos."""
        return [self.serialize_doc(doc) for doc in cur]

    def serialize_doc(self, doc):
        """Serializa un solo documento."""
        return json.loads(json.dumps(doc, default=self.default_serializer))

