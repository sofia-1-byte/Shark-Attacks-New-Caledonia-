import sqlite3
import pandas as pd

base_de_datos = "/BBDD/shark_attacks.db"
tabla = "shark_attacks"


# para conectar bbdd
def conectar_bd():

    try:
        conexion = sqlite3.connect(base_de_datos)
        print(f"Conectado a: {base_de_datos}")
        return conexion
    except Exception as e:
        print(f"Error conectando a la base de datos: {e}")
        return None

# para cargar datos
def cargar_datos(tabla):

    conexion = conectar_bd()
    if conexion:

        try:
            query = f"SELECT * FROM {tabla};"
            datos = pd.read_sql_query(query, conexion)
            print(f"Datos cargados: {len(datos)} registros de {tabla}")
            return datos
        except Exception as e:
            print(f" Error cargando datos: {e}")
            return None
        finally:
            conexion.close()
    else:
        return None

# para obtener tablas disponibles
def obtener_tablas_disponibles():

    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tablas = [tabla[0] for tabla in cursor.fetchall()]
            print(f" Tablas disponibles en la base de datos:")
            for tabla in tablas:
                print(f"   - {tabla}")
            return tablas
        except Exception as e:
            print(f"Error obteniendo tablas: {e}")
            return []
        finally:
            conexion.close()
    return []

