from wtforms import Form
from wtforms import SelectField


class CiudadesForm(Form):
    origen = SelectField("origen")
    destino = SelectField("destino")
