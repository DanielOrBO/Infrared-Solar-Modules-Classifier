from sshtunnel import SSHTunnelForwarder
import pandas as pd
import pymysql

## DEFINICION DE VARIABLES

ssh_ip_address = 'elektra.udea.edu.co'
ssh_p_username = 'solarudea'
ssh_p_password = "ElCoco2022"
ssh_port = 22
ssh_remote_bind_address = 3306
db_server_ip = 'elektra.udea.edu.co'
db_server_port = 3306
db_user = 'solarudea'
db_user_password = 'canoquintero'
db_name = 'termografia'

## CONEXION SSH

tunnel = SSHTunnelForwarder((ssh_ip_address, 22), ssh_password=ssh_p_password, ssh_username=ssh_p_username,
                            remote_bind_address=('127.0.0.1', 3306))
tunnel.start()

# CONEXION MYSQL
db = pymysql.connect(host='localhost', port=tunnel.local_bind_port, user=ssh_p_username,
                          passwd=db_user_password, db=db_name)
cur = db.cursor()
cur.execute("SELECT * FROM imagenes limit 10;")
cur.close()

# CREAR DATAFRAME EN PANDAS
df = pd.DataFrame(cur.fetchall())
df.columns = [i[0] for i in cur.description]

# IMPRIMIR RESULTADO
print(df)