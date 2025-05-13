# -*- coding: UTF-8 -*-
import os
import inspect
import yaml
import re

from run.runweb import Server

def extract_endpoint_info(method):
    """Extrae información del endpoint a partir de su documentación y código"""
    doc = inspect.getdoc(method)
    params = []
    description = "Sin descripción"
    
    if doc:
        description = doc
    
    # Extraer parámetros de la firma del método
    sig = inspect.signature(method)
    for param_name, param in sig.parameters.items():
        if param_name != 'self' and param_name != 'kwargs' and param_name != 'args':
            # Determinar si es requerido
            required = param.default == inspect.Parameter.empty
            
            # Determinar tipo
            param_type = "string"
            if param.annotation != inspect.Parameter.empty:
                if param.annotation == int:
                    param_type = "integer"
                elif param.annotation == bool:
                    param_type = "boolean"
            
            params.append({
                "name": param_name,
                "in": "query",
                "required": required,
                "schema": {
                    "type": param_type
                },
                "description": f"Parámetro {param_name}"
            })
    
    # Inferir método HTTP
    http_method = "get"
    source_code = inspect.getsource(method)
    if '@cherrypy.tools.allow' in source_code:
        method_match = re.search(r'methods=\["([A-Z]+)"\]', source_code)
        if method_match:
            http_method = method_match.group(1).lower()
    
    return {
        "summary": f"Endpoint {method.__name__}",
        "description": description,
        "parameters": params,
        "responses": {
            "200": {
                "description": "Operación exitosa"
            },
            "500": {
                "description": "Error interno del servidor"
            }
        }
    }

def generate_openapi_schema():
    """Genera el esquema OpenAPI basado en los endpoints registrados"""
    # Estructura base del esquema OpenAPI
    schema = {
        "openapi": "3.0.0",
        "info": {
            "title": "Genobank API",
            "description": "API para gestión de permisos, perfiles, biosamples y servicios relacionados",
            "version": "1.0.0"
        },
        "servers": [
            {
                "url": "http://localhost:8080",
                "description": "Servidor de desarrollo"
            }
        ],
        "paths": {},
        "components": {
            "schemas": {
                "Error": {
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "example": "Failure"
                        },
                        "status_details": {
                            "type": "object",
                            "properties": {
                                "message": {
                                    "type": "string",
                                    "description": "Mensaje de error"
                                },
                                "description": {
                                    "type": "string",
                                    "description": "Descripción detallada del error"
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    
    # Busca los métodos expuestos en la clase Server
    server_methods = inspect.getmembers(Server, predicate=inspect.isfunction)
    
    for name, method in server_methods:
        source = inspect.getsource(method)
        if '@cherrypy.expose' in source and name != 'api_docs' and name != 'options':
            # Es un endpoint expuesto
            endpoint_info = extract_endpoint_info(method)
            
            # Determina el método HTTP
            http_method = "get"  # Por defecto
            if '@cherrypy.tools.allow' in source:
                method_match = re.search(r'methods=\["([A-Z]+)"\]', source)
                if method_match:
                    http_method = method_match.group(1).lower()
            
            # Añade la ruta al esquema
            path = f"/{name}"
            if path not in schema["paths"]:
                schema["paths"][path] = {}
            
            schema["paths"][path][http_method] = endpoint_info
    
    # Guarda el esquema en un archivo YAML
    with open("openapi.yaml", "w") as f:
        yaml.dump(schema, f, default_flow_style=False)
    
    print(f"Esquema OpenAPI generado en openapi.yaml")
    return schema

if __name__ == "__main__":
    generate_openapi_schema()