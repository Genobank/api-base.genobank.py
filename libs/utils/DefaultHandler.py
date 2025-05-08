import cherrypy

class DefaultHandler:
    exposed = True  # Hace que todos los métodos estén expuestos para CherryPy

    def _cp_dispatch(self, vpath):
        if len(vpath) == 1:
            cherrypy.request.params['serial'] = vpath.pop()  # Asume que es el parámetro 'serial'
            return self

        return vpath

    def __call__(self, *args, **kwargs):
        method = cherrypy.request.method.upper()
        handler = getattr(self, method.lower(), None)

        if callable(handler):
            return handler(*args, **kwargs)
        else:
            raise cherrypy.HTTPError(405, f'Method {method} not allowed.')
