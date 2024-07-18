import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash


class Usuario:
    def __init__(self, nombres, apellidos, correo_electronico, contrasena, fecha_de_nacimiento, cedula_identidad):
        self.nombres = nombres
        self.apellidos = apellidos
        self.correo_electronico = correo_electronico
        self.contrasena = contrasena  # La contraseña se pasa aquí en texto plano y se hashea en agregar_usuario
        self.fecha_de_nacimiento = fecha_de_nacimiento
        self.cedula_identidad = cedula_identidad

    def verificar_contrasena(self, contrasena_plana):
        return check_password_hash(self.contrasena, contrasena_plana)


def conectar_bd():
    try:
        return mysql.connector.connect(
            database='crud_usuarios',
            user='root',  # Cambia esto a tu usuario de MySQL
            password='adminkvn-12345',  # Usar variable de entorno para mayor seguridad
            host='localhost',
            port='3306'  # Puerto predeterminado de MySQL
        )
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def inicializar_bd():
    conn = conectar_bd()
    if conn is not None:
        try:
            with conn.cursor() as cursor:
                cursor.execute("""CREATE TABLE IF NOT EXISTS Usuarios (
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    nombres VARCHAR(255) NOT NULL,
                                    apellidos VARCHAR(255) NOT NULL,
                                    correo_electronico VARCHAR(255) NOT NULL UNIQUE,
                                    contrasena VARCHAR(255) NOT NULL,
                                    fecha_de_nacimiento DATE NOT NULL,
                                    cedula_identidad VARCHAR(20) NOT NULL UNIQUE)""")
                conn.commit()
        except Error as e:
            print(f"Error al inicializar la base de datos: {e}")
        finally:
            conn.close()

def agregar_usuario(usuario):
    conn = conectar_bd()
    if conn is not None:
        try:
            with conn.cursor() as cursor:
                contrasena_hash = generate_password_hash(usuario.contrasena)
                cursor.execute("""INSERT INTO Usuarios (nombres, apellidos, correo_electronico, contrasena, fecha_de_nacimiento, cedula_identidad)
                                  VALUES (%s, %s, %s, %s, %s, %s)""",
                               (usuario.nombres, usuario.apellidos, usuario.correo_electronico, contrasena_hash, usuario.fecha_de_nacimiento, usuario.cedula_identidad))
                conn.commit()
        except Error as e:
            print(f"Error al agregar usuario: {e}")
        finally:
            conn.close()

def obtener_usuario_por_correo(correo_electronico):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("""SELECT id_usuario, nombres, apellidos, correo_electronico, contrasena, fecha_de_nacimiento, cedula_identidad 
                      FROM Usuarios WHERE correo_electronico = %s""", (correo_electronico,))
    usuario_data = cursor.fetchone()
    conn.close()
    if usuario_data:
        usuario = Usuario(usuario_data[1], usuario_data[2], usuario_data[3], usuario_data[4], usuario_data[5], usuario_data[6])
        usuario.id = usuario_data[0]  # Asigna el id después de la creación
        return usuario
    return None

def existe_usuario(correo_electronico):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Usuarios WHERE correo_electronico = %s", (correo_electronico,))
    existe = cursor.fetchone() is not None
    conn.close()
    return existe

# Inicializar la base de datos al arrancar la aplicación
inicializar_bd()
