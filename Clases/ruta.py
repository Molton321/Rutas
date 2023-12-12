class Ruta:
    def __init__(self, codigo, origen, destino, distancia, tiempo):
        self._codigo = codigo
        self._origen = origen
        self._destino = destino
        self._distancia = distancia
        self._tiempo = tiempo
    
    
    def get_codigo(self):
        return self._codigo
    
    def set_codigo(self, codigo):
        self._codigo = codigo
    
    def get_origen(self):
        return self._origen
    
    def set_origen(self, origen):
        self._origen = origen
        
    def get_destino(self):
        return self._destino
    
    def set_destino(self, destino):
        self._destino = destino
        
    def get_distancia(self):
        return self._distancia
    
    def set_distancia(self, distancia):
        self._distancia = distancia
        
    def get_tiempo(self):
        return self._tiempo
    
    def set_tiempo(self, tiempo):
        self._tiempo = tiempo