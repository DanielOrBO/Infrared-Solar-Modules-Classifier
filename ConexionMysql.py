import mysql.connector #Importamos la libreria para conectarnos.
from sshtunnel import SSHTunnelForwarder
import pandas as pd
import pymysql
###################################### CREACIÓN Y CONEXIÓN ######################################

"""
Creamos conexión a la base de datos, en esta debemos enviar parámetros
host = "localhost"
user = "root"
password = ""
port = "3306" # Se puede omitir (lo comentamos), se coloca por defecto
database = ""
"""
conn =  mysql.connector.connect(
    host = 'elektra.udea.edu.co',
    user = "solarudea",
    password = "ElCoco2022",
    #port = "3306" # Se puede omitir (lo comentamos), se coloca por defecto
    # database = ""
)

# El cursor es el que nos permite interactuar con la bbdd
cursor = conn.cursor()

# PASO 1 OBSERVAR QUE BD TENEMOS
cursor.execute("SHOW DATABASES") # El comando execute pasa unos métodos de SQL a la base de datos
for bd in cursor: # Extraer información que está en el cursor es decir las bbdd
    print(bd)

# cursor.execute("CREATE DATABASE Paneles_img")


######################################################## Crear tablas en bd ############################################################

# query = """
# CREATE TABLE imagenes (
# image_filepath VARCHAR(200),
# anomaly_class VARCHAR(200),
# """
# for i in range(1000):
#     query = query + ' Columna_' + str(i) + ' float(15, 14), \n'

# query = query[:-3] + ');'

# cursor.execute(query)

# # ############################################## Agregamos las 1000 columnas ####################################################
# for i in range (0,5):
#     sql = """ALTER TABLE FEATURES ADD COLUMN column_{} FLOAT""".format(str(i)) 
#     cursor.execute(sql)

####################################### Comando para borrar tabla por si nos equivocamos ##########################################
    

# sql = """DROP TABLE FEATURES"""
# cursor.execute(sql)
# conn.commit()


# ########################################### Cerramos conexión y guardamos cambios ###############################################
conn.commit()
conn.close()
