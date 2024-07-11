import mysql.connector
from mysql.connector import Error

class DBHelper:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                print('Conexión exitosa')
        except Error as ex:
            print(f'Error de MySQL: {ex}')
            raise

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print('Conexión cerrada')

# Uso de la clase DBHelper
db = DBHelper('localhost', 'crud_usuarios', 'root', 'adminkvn-12345')
db.connect()
# Realizar operaciones con la base de datos
db.close()

