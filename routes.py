from libs.handlers.example import ExampleHandler
from libs.handlers.permittee_handler import PermitteeHandler

ROUTES = [
    ('/example', ExampleHandler),
    ('/permittees', PermitteeHandler),
]
