class Aeropuerto:
    def __init__(self, nombre, ubicacion, codigo):
        self._nombre = nombre
        self._ubicacion = ubicacion
        self._codigo = codigo
        
    def get_nombre(self):
        return self._nombre
    
    def set_nombre(self, nombre):
        self._nombre = nombre
    
    def get_ubicacion(self):
        return self._ubicacion
    
    def set_ubicacion(self, ubicacion):
        self._ubicacion = ubicacion
        
    def get_codigo(self):
        return self._codigo
    
    def set_codigo(self, codigo):
        self._codigo = codigo