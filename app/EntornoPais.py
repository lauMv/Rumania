from AgenteIA.Entorno import Entorno


class EntornoPais(Entorno):

    def __init__(self):
        Entorno.__init__(self)
        self.ciudades = {}
        self.distancias = {}
        self.lineal = {}

    def agregar(self, c):
        self.ciudades[c] = []

    def conectar(self, ori, dest, costo):
        self.ciudades[ori].append(dest)
        self.ciudades[dest].append(ori)
        self.distancias[(ori, dest)] = costo
        self.distancias[(dest, ori)] = costo

    def percibir(self, agente):
        agente.dis = self.distancias
        agente.lineal = self.lineal
        agente.percepciones = self.ciudades
        agente.programa()
        agente.vive = False

    def distancia_lineal(self, ciudad, distancia):
        self.lineal[ciudad] = distancia

    def ejecutar(self, agente):
        for a in agente.acciones:
            print(a, " ",)

