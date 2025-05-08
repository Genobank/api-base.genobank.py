import cherrypy

class DomainInjectionError(Exception):    
	def __init__(self,_service_classname,_domain_classname):
		msg = "Input object in service {0} is not of type {1}".format(_service_classname,_domain_classname)
		super(DomainInjectionError, self).__init__(msg)