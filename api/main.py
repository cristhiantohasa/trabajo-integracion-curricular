from flask import Flask
from flask import Request
import xmltodict
import json
import pyodbc

app = Flask( __name__ )

#Insertar Datos
@app.route('/salvadatos/insertarDatos', methods=["POST"])
def insertarDatos():

    with open("resources/datos.xml", 'r') as xmlDatos:
        jsonRoot = xmltodict.parse(xmlDatos.read())

    jsonRoot = json.dumps(jsonRoot)
    jsonRoot = json.loads(jsonRoot)

    jsonDatos = jsonRoot['root']

    jsonPersona = jsonDatos['persona']
    jsonContacto = jsonDatos['contacto']
    jsonDatosPersonales = jsonDatos['datosPesonales']
    jsonEmpelador = jsonDatos['empleador']
    jsonHistorial = jsonDatos['historial']

    cedula = jsonPersona['cedula']
    nombres = jsonPersona['nombres']
    apellidos = jsonPersona['apellidos']
    sexo = jsonPersona['sexo']
    condicionCiudadano = jsonPersona['condicionCiudadano']
    fechaNacimiento = jsonPersona['fechaNacimiento']
    lugarNacimiento = jsonPersona['lugarNacimiento']
    nacionalidad = jsonPersona['nacionalidad']
    estadoCivil = jsonPersona['estadoCivil']
    codigoDactilar = jsonPersona['codigoDactilar']

    domicilio = jsonContacto['domicilio']
    callesDomicilio = jsonContacto['callesDomicilio']
    numeroCasa = jsonContacto['numeroCasa']
    telefono = jsonContacto['telefono']
    correoElectronico = jsonContacto['correoElectronico']

    try:
        
        connection = pyodbc.connect('DRIVER={SQL Server};SERVER=SERVER1;DATABASE=Registro_Civil_EPN;UID=sa;PWD=smile')
        print("Conexión exitosa...")

        qrRegistroCivil = 'EXEC sp_insertarDatos \'' + cedula + '\', \'' + nombres + '\', \'' + apellidos + '\', \'' + sexo + '\', \'' + condicionCiudadano + '\', \'' + fechaNacimiento + '\', \'' + lugarNacimiento + '\', \'' + nacionalidad + '\', \'' + estadoCivil + '\', \'' + codigoDactilar + '\', \'' + domicilio + '\', \'' + callesDomicilio + '\', \'' + numeroCasa + '\', \'' + telefono + '\', \'' + correoElectronico + '\''
        print(qrRegistroCivil)

        cursorInsert = connection.cursor()

        cursorInsert.execute(qrRegistroCivil)
        cursorInsert.commit()

    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
    finally:
        connection.close()  # Se cerró la conexión a la BD.
        print("La conexión ha finalizado.")

    return jsonDatos;

# Obtener Datos
@app.route('/salvadatos/obtenerDatos', methods=["GET"])
def obtenerDatos():

    print("Get");

    return "Hola Mundo :D";

app.run( debug = True );