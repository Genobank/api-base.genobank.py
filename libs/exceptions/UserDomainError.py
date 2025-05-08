import cherrypy

class UserDomainError(Exception):
    def __init__(self,msg):
        super(UserDomainError, self).__init__(msg)