import mysql.connector
from mysql.connector import Error
import base64
from Usuarios_grupo9.conexion.unionDB import DBHelper

#Recibe la instancia que maneja la base de datos
class CRUDOperations:
    def __init__(self, db_helper):
        self.db_helper = db_helper

#Crear nuevo usuario
    def createUsuario(self, nombres, apellidos, correo_electronico, contrasena, fecha_de_nacimiento, cedula_identidad):

        try:
            #Creo una instancia en el cursor
            cursor = self.db_helper.connection.cursor()
            cursor.execute("""
                INSERT INTO Usuarios (nombres, apellidos, correo_electronico, contrasena, fecha_de_nacimiento, cedula_identidad)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (nombres, apellidos, correo_electronico, contrasena, fecha_de_nacimiento, cedula_identidad))
            # Confirmar la transacción
            self.db_helper.connection.commit()

            # Devolver un mensaje de éxito
            return {'message': 'Usuario creado exitosamente'}

        except Error as ex:
            print(f'Error de MySQL: {ex}')
            raise

        finally:
            # Cerrar el cursor
            cursor.close()

#Eliminar usuarios
    def delete_usuario(self, id_usuario):
        try:
            cursor = self.db_helper.connection.cursor()

            # Eliminar usuario por ID
            cursor.execute("DELETE FROM Usuarios WHERE id_usuario = %s", (id_usuario,))

            # Confirmar la transacción
            self.db_helper.connection.commit()

        except Error as ex:
            print(f'Error de pyodbc: {ex}')
            raise

        finally:
            # Cerrar el cursor
            cursor.close()

#Para devolver todos los usuarios
    def read_all_usuarios(self):
        try:
            # Crear una instancia de cursor
            cursor = self.db_helper.connection.cursor(dictionary=True)

            # Ejecutar la consulta para obtener todos los usuarios
            cursor.execute(
                "SELECT id_usuario, nombres, apellidos, correo_electronico, contrasena, fecha_de_nacimiento, cedula_identidad FROM Usuarios")

            # Obtener todas las filas resultantes
            usuarios = cursor.fetchall()

            return usuarios

        except mysql.connector.Error as ex:
            print(f'Error de MySQL: {ex}')
            raise

        finally:
            # Cerrar el cursor
            if 'cursor' in locals() and cursor is not None:
                cursor.close()

#Actualizar un usuario existente
    def update_usuario(self, id_usuario, nombres, apellidos, correo_electronico, contrasena, fecha_de_nacimiento, cedula_identidad):
        try:
            # Crear una instancia de cursor
            cursor = self.db_helper.connection.cursor()

            cursor.execute("""
                      UPDATE Usuarios
                      SET nombres = %s, apellidos = %s, correo_electronico = %s, contrasena = %s, fecha_de_nacimiento = %s, cedula_identidad = %s
                      WHERE id_usuario = %s
                   """, (
            nombres, apellidos, correo_electronico, contrasena, fecha_de_nacimiento, cedula_identidad, id_usuario))

            # Confirmar la transacción
            self.db_helper.connection.commit()

            # Devolver un mensaje de éxito
            return {'message': 'Usuario actualizado exitosamente'}

        except Error as ex:
            print(f'Error de pyodbc: {ex}')
            raise

        finally:
            # Cerrar el cursor
            cursor.close()

#Validaciones para el login
    def find_usuario_by_credentials(self, correo_electronico, contrasena):
        try:
            # Crear una instancia de cursor
            cursor = self.db_helper.connection.cursor()

            # Ejecutar la consulta para buscar un usuario por correo electrónico y contraseña
            cursor.execute("""
                SELECT *
                FROM Usuarios
                WHERE correo_electronico = %s AND contrasena = %s
            """, (correo_electronico, contrasena))

            # Obtener el primer usuario que coincida (o None si no hay coincidencias)
            usuario = cursor.fetchone()

            # Si se encontró un usuario, devolverlo en un formato adecuado
            if usuario:
                result = {
                    'id_usuario': usuario[0],
                    'nombres': usuario[1],
                    'apellidos': usuario[2],
                    'correo_electronico': usuario[3],
                    'contrasena': usuario[4],
                    'fecha_de_nacimiento': usuario[5],
                    'cedula_identidad': usuario[6]
                }
                return result
            else:
                return None

        except Error as ex:
            print(f'Error de MySQL: {ex}')
            raise

        finally:
            # Cerrar el cursor
            cursor.close()

#Obtener un usuario por medio de su ID
    def get_usuario_by_id(self, id_usuario):
        try:
            cursor = self.db_helper.connection.cursor()

            # Ejecutar la consulta para obtener un usuario por su ID
            cursor.execute("""
                SELECT id_usuario, nombres, apellidos, correo_electronico, contrasena, fecha_de_nacimiento, cedula_identidad
                FROM Usuarios
                WHERE id_usuario = %s
            """, (id_usuario,))

            # Obtener el usuario si existe
            usuario = cursor.fetchone()

            # Si se encuentra el usuario, devolver sus detalles
            if usuario:
                usuario_data = {
                    'id_usuario': usuario[0],
                    'nombres': usuario[1],
                    'apellidos': usuario[2],
                    'correo_electronico': usuario[3],
                    'contrasena': usuario[4],
                    'fecha_de_nacimiento': usuario[5],
                    'cedula_identidad': usuario[6],
                }

                return usuario_data
            else:
                return None

        except Error as ex:
            print(f'Error de MySQL: {ex}')
            raise

        finally:
            cursor.close()