from AgenteIA.AgenteBuscador import AgenteBuscador
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

class AgenteViajero(AgenteBuscador):

    def __init__(self):
        AgenteBuscador.__init__(self)
        self.dis = {}
        self.lineal = {}

    def genera_hijos(self, nodo):
        return self.percepciones[nodo]

    def get_costo(self, camino):
        return sum([self.dis[(camino[i], camino[i + 1])] for i in range(len(camino) - 1)])

    def get_heuristica(self, camino):
        geo_data = Nominatim(user_agent="geo_data")
        l1 = geo_data.geocode(camino[0])
        l2 = geo_data.geocode(self.estadoMeta)
        ciudad_origen = (l1.latitude, l1.longitude)
        ciudad_destino = (l2.latitude, l2.longitude)
        distancia_lineal = geodesic(ciudad_origen, ciudad_destino).kilometers
        return distancia_lineal

    def get_funcion_a(self, camino):
        return self.get_costo(camino) + self.get_heuristica(camino)