from flask import Flask;
from flask import Request;
import xmltodict;
import json;
import pyodbc;

try:
    connection = pyodbc.connect('DRIVER={SQL Server};SERVER=SERVER1;DATABASE=Registro_Civil_EPN;UID=sa;PWD=smile')
    print("Conexión exitosa.")
except Exception as ex:
    print("Error durante la conexión: {}".format(ex))
finally:
    connection.close()  # Se cerró la conexión a la BD.
    print("La conexión ha finalizado.")


app = Flask( __name__ );

#Insertar Datos
@app.route('/salvadatos/insertarDatos', methods=["POST"])
def obtenerDatos():

    with open("resources/datos.xml", 'r') as xmlDatos:
        jsonDatos = xmltodict.parse(xmlDatos.read());

    jsonDatos = json.dumps(jsonDatos);
    jsonDatos = json.loads(jsonDatos);



    return jsonDatos;

# Obtener Datos
@app.route('/salvadatos/obtenerDatos', methods=["GET"])
def insertarDatos():

    print("Get");

    return "Hola Mundo :D";

app.run( debug = True );