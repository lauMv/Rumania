#################################################################
# Nombre      : Agente Buscador                                 #
# Version     : 0.05.03.2017                                    #
# Autor       : Victor                                          #
# Descripcion : Clase especificacion de Agente, implementa      #
#               algoritmos de busqueda                           #
##################################################################


from AgenteIA.Agente import Agente
from copy import deepcopy
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from app import Forms


class AgenteBuscador(Agente):

    def __init__(self):
        Agente.__init__(self)
        self.dis = {}
        self.lineal = {}
        self.funcionSucesor = []
        self.tecnica = None
        self.estadoInicial = None
        self.estadoMeta = None
        self.acciones = None

    def set_tecnica(self, t):
        self.tecnica = t

    def set_estado_inicial(self, e0):
        self.estadoInicial = e0

    def set_estado_meta(self, ef):
        self.estadoMeta = ef

    def add_funcion_sucesor(self, fun):
        self.funcionSucesor.append(fun)

    def test_objetivo(self, nodo):
        return nodo == self.estadoMeta

    def genera_hijos(self, nodo):
        raise Exception('Se debe implementar generación de hijos')

    def get_costo(self, camino):
        return len(camino)

      # def get_heuristica(self, camino):

    #     costo = 0
    #     for x in range(len(camino)-1):
    #         costo += self.lineal[self.get_dist(camino[x]),self.get_dist(camino[x+1])]
    #     return costo

    def get_heuristica(self, camino):
        geo_data = Nominatim(user_agent="geo_data")
        l1 = geo_data.geocode(camino[0])
        l2 = geo_data.geocode(self.estadoMeta)
        ciudad_origen = (l1.latitude, l1.longitude)
        ciudad_destino = (l2.latitude, l2.longitude)
        distancia_lineal = geodesic(ciudad_origen, ciudad_destino).kilometers
        return distancia_lineal

    def get_funcion_a(self, camino):
        return self.get_costo(camino)+self.get_heuristica(camino)

    def programa(self):
        frontera = [[self.estadoInicial]]
        visitados = []
        cont = 0
        while frontera:
            cont += 1

            if self.tecnica == "profundidad":
                camino = frontera.pop()
            else:
                camino = frontera.pop(0)
            nodo = camino[-1]
            if self.test_objetivo(nodo):
                self.acciones = camino
                break
            else:
                visitados.append(nodo)
                for hijo in self.genera_hijos(nodo):
                    if hijo != 0 and not (hijo in visitados):
                        aux = deepcopy(camino)
                        aux.append(hijo)
                        frontera.append(aux)

                if self.tecnica == "costouniforme":
                    frontera.sort(key=lambda tup: self.get_costo(tup))
                elif self.tecnica == "codicioso":
                    frontera.sort(key=lambda tup: self.get_heuristica(tup))
                elif self.tecnica == "A*":
                    frontera.sort(key=lambda tup: self.get_funcion_a(tup))
