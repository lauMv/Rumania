from flask import Flask
from flask import render_template
from app import Forms
from flask import request
from app.EntornoPais import EntornoPais
from app.AgenteViajero import AgenteViajero
from geopy.geocoders import Nominatim
from geopy.distance import geodesic


app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    acciones = []
    distancia = ""
    distancia_lineal = ""

    # configuramos nuestro entorno, en este caso Mapa de rumania
    rumania = EntornoPais()
    # agregamos las ciudades
    rumania.agregar("Arad")
    rumania.agregar("Timișoara")
    rumania.agregar("Zerind")
    rumania.agregar("Oradea")
    rumania.agregar("Sibiu")
    rumania.agregar("Lugoj")
    rumania.agregar("Mehadia")
    rumania.agregar("Drobeta")
    rumania.agregar("Craiova")
    rumania.agregar("Rimnicu")
    rumania.agregar("Fagaras")
    rumania.agregar("Pitesti")
    rumania.agregar("Bucarest")
    rumania.agregar("Giurgiu")
    rumania.agregar("Urziceni")
    rumania.agregar("Hirsova")
    rumania.agregar("Eforie")
    rumania.agregar("Vaslui")
    rumania.agregar("Iasi")
    rumania.agregar("Neamt")
    # conectamos bidireccionalmente las ciudades
    rumania.conectar("Arad", "Zerind", 75)
    rumania.conectar("Arad", "Sibiu", 140)
    rumania.conectar("Arad", "Timișoara", 118)
    rumania.conectar("Zerind", "Oradea", 71)
    rumania.conectar("Sibiu", "Fagaras", 99)
    rumania.conectar("Sibiu", "Rimnicu", 80)
    rumania.conectar("Timișoara", "Lugoj", 111)
    rumania.conectar("Oradea", "Sibiu", 151)
    rumania.conectar("Fagaras", "Bucarest", 211)
    rumania.conectar("Rimnicu", "Pitesti", 97)
    rumania.conectar("Rimnicu", "Craiova", 146)
    rumania.conectar("Lugoj", "Mehadia", 70)
    rumania.conectar("Mehadia", "Drobeta", 75)
    rumania.conectar("Pitesti", "Bucarest", 101)
    rumania.conectar("Drobeta", "Craiova", 120)
    rumania.conectar("Craiova", "Pitesti", 138)
    rumania.conectar("Bucarest", "Giurgiu", 90)
    rumania.conectar("Bucarest", "Urziceni", 85)
    rumania.conectar("Urziceni", "Hirsova", 85)
    rumania.conectar("Hirsova", "Eforie", 86)
    rumania.conectar("Urziceni", "Vaslui", 142)
    rumania.conectar("Vaslui", "Iasi", 92)
    rumania.conectar("Iasi", "Neamt", 87)

    # incorporamos el formulario (app/Forms)
    local_form = Forms.CiudadesForm(request.form)
    # cargamos las ciudades de nuestro mapa en los combo box
    local_form.origen.choices = [(o, o) for o in rumania.ciudades.keys()]
    local_form.destino.choices = [(o, o) for o in rumania.ciudades.keys()]
    # verificamos si se esta enviando las ciudades seleccionadas del combobox al formulario
    if request.method == 'POST':
        # computar distancia lineal de la ciudad origen a ciudad destino
        # esta debe ser nuestra heuristica, debemos implementarla en el agente.
        geo_data = Nominatim(user_agent="geo_data")
        # capturar información geo
        l1 = geo_data.geocode(local_form.origen.data)
        l2 = geo_data.geocode(local_form.destino.data)
        ciudad_origen = (l1.latitude, l1.longitude)
        ciudad_destino = (l2.latitude, l2.longitude)
        # computar distancia
        distancia_lineal = geodesic(ciudad_origen, ciudad_destino).kilometers

        # instanciamos nuestro agente viajero
        bus = AgenteViajero()
        bus.set_estado_inicial(local_form.origen.data)
        bus.set_estado_meta(local_form.destino.data)
        # seleccionamos la tecnica
        # bus.set_tecnica("costouniforme")
        # bus.set_tecnica("codicioso")
        bus.set_tecnica("A*")
        # insertamos nuestro agente
        rumania.insertar_objeto(bus)
        # ejecutamos nuestro agente
        rumania.run()
        # mostramos el camino encontrado por el agente
        acciones = bus.acciones
        distancia = bus.get_costo(bus.acciones)
        # enviamos a la pagina index.html, formulario y los datos computados
    return render_template("index.html", form=local_form,
                           acciones=acciones,
                           distancia=distancia,
                           distancia_lineal=distancia_lineal)


if __name__ == '__main__':
    # ejecutamos nuestro servidor http en el puerto 5000
    # http://localhost:5000
    app.run(debug=True)
