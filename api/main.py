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

    estadoAfiliado = jsonDatosPersonales['estadoAfiliado']
    
    rucPatronal = jsonEmpelador['rucPatronal']
    sector = jsonEmpelador['sector']
    razonSocial = jsonEmpelador['razonSocial']
    
    origen = jsonHistorial['origen']
    periodoDesde = jsonHistorial['periodoDesde']
    periodoHasta = jsonHistorial['periodoHasta']
    imposiciones = jsonHistorial['imposiciones']
    dias = jsonHistorial['dias']

    try:
        
        connection = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=SERVER1;DATABASE=Registro_Civil_EPN;UID=sa;PWD=smile'
            )
        print("Conexión exitosa...")

        qrInsertRegistroCivil = 'EXEC [SERVER1].[Registro_Civil_EPN].[dbo].[sp_insertarDatosRegistroCivil] \'' + cedula + '\', \'' + nombres + '\', \'' + apellidos + '\', \'' + sexo + '\', \'' + condicionCiudadano + '\', \'' + fechaNacimiento + '\', \'' + lugarNacimiento + '\', \'' + nacionalidad + '\', \'' + estadoCivil + '\', \'' + codigoDactilar + '\', \'' + domicilio + '\', \'' + callesDomicilio + '\', \'' + numeroCasa + '\', \'' + telefono + '\', \'' + correoElectronico + '\''
        print(qrInsertRegistroCivil)

        cursorInsert = connection.cursor()

        cursorInsert.execute(qrInsertRegistroCivil)
        cursorInsert.commit()

        response = 'Insercion Registro Civil exitosa ' + cedula

    except Exception as ex:

        print("Error durante la conexión: {}".format(ex))
        response = 'Error de conexion Registro Civil'

    finally:

        connection.close()  # Se cerró la conexión a la BD.
        print("La conexión Registro Civil ha finalizado.")

    try:
        
        connection = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=SERVER2;DATABASE=IEES_EPN;UID=sa;PWD=smile'
            )
        print("Conexión exitosa...")
        
        qrInsertIEES = 'EXEC [SERVER2].[IEES_EPN].[dbo].[sp_insertarDatosIEES] \'' + cedula + '\', \'' + estadoAfiliado + '\', \'' + rucPatronal + '\', \'' + sector + '\', \'' + razonSocial + '\', \'' + origen + '\', \'' + periodoDesde + '\', \'' + periodoHasta + '\', ' + imposiciones + ', ' + dias
        print(qrInsertIEES)

        cursorInsert = connection.cursor()

        cursorInsert.execute(qrInsertIEES)
        cursorInsert.commit()

        response = '\nInsercion IEES exitosa ' + cedula

    except Exception as ex:

        print("Error durante la conexión: {}".format(ex))
        response = ' \nError de conexionen IEES'

    finally:

        connection.close()  # Se cerró la conexión a la BD.
        print("La conexión IEES ha finalizado.")

    return response;

# Obtener Datos
@app.route('/salvadatos/obtenerDatos', methods=["GET"])
def obtenerDatos():

    try:

        connection = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=SERVER1;DATABASE=Salva_Datos_EPN;UID=sa;PWD=smile'
            )
        print("Conexión exitosa...")

        qrSelectSalvaDatos = 'SELECT * FROM v_obtenerDatosNivelCinco'
        print(qrSelectSalvaDatos)

        cursorSelect = connection.cursor()

        cursorSelect.execute(qrSelectSalvaDatos)

        rows = cursorSelect.fetchall()

        rows = [tuple(row) for row in rows]
        rows = json.dumps(rows)

        response = rows

    except Exception as ex:

        print("Error durante la conexión: {}".format(ex))
        response = 'Error de conexion'

    finally:
        connection.close()  # Se cerró la conexión a la BD.
        print("La conexión ha finalizado.")

    return response;

app.run( debug = True );