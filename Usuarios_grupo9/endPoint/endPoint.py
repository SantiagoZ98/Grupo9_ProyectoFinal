from flask import Flask, jsonify, request
from flask_cors import CORS
from Usuarios_grupo9.conexion.unionDB import DBHelper
from Usuarios_grupo9.CRUDS.crudUsers import CRUDOperations
#from Usuarios_grupo9.InteligenciArtif.Consulta import InferenceService
from flask_jwt_extended import create_access_token
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'Kvnsnt2210'
CORS(app,  origins='http://localhost:3000')
jwt = JWTManager(app)

# Configuración de la base de datos
db_helper = DBHelper(host='localhost',
                     database='crud_usuarios',
                     user='root',
                     password='adminkvn-12345')

# Inicializar la clase CRUDOperations con el objeto DBHelper
crud_usuarios = CRUDOperations(db_helper)

#inference_service = InferenceService()

# Endpoint create_new_usuario
@app.route('/api/usuarios', methods=['POST'])
def create_new_usuario():
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.get_json()

        # Validar que todos los campos requeridos estén presentes
        required_fields = ['nombres', 'apellidos', 'correo_electronico', 'contrasena', 'fecha_de_nacimiento',
                           'cedula_identidad']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Todos los campos son requeridos: {field}'}), 400

        nombres = data['nombres']
        apellidos = data['apellidos']
        correo_electronico = data['correo_electronico']
        contrasena = data['contrasena']
        fecha_de_nacimiento = data['fecha_de_nacimiento']
        cedula_identidad = data['cedula_identidad']

        # Conectar a la base de datos
        db_helper.connect()

        # Crear un nuevo usuario
        result = crud_usuarios.createUsuario(nombres, apellidos, correo_electronico, contrasena, fecha_de_nacimiento,
                                             cedula_identidad)

        # Devolver el resultado como respuesta
        return jsonify(result)

    except Exception as ex:
        # Manejar otros errores
        return jsonify({'error': str(ex)}), 500
    finally:
        # Cerrar la conexión
        if db_helper.connection:
            db_helper.close()

# Endpoint para eliminar un usuario por ID
@app.route('/api/usuarios/<int:id_usuario>', methods=['DELETE'])
def delete_usuario(id_usuario):
    try:
        # Conectar a la base de datos
        db_helper.connect()

        # Eliminar el usuario por ID
        crud_usuarios.delete_usuario(id_usuario)

        return jsonify({'message': 'Usuario eliminado correctamente'})

    except Exception as ex:
        # Manejar errores
        return jsonify({'error': str(ex)}), 500

    finally:
        # Cerrar la conexión
        db_helper.close()

# Endpoint para actualizar un usuario por ID
@app.route('/api/usuarios/<int:id_usuario>', methods=['PUT'])
def update_usuario(id_usuario):
    try:
        # Conectar a la base de datos
        db_helper.connect()

        # Obtener datos del cuerpo de la solicitud
        data = request.get_json()

        # Validar que todos los campos necesarios están presentes
        required_fields = ['nombres', 'apellidos', 'correo_electronico', 'contrasena', 'fecha_de_nacimiento',
                           'cedula_identidad']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Falta el campo requerido: {field}'}), 400

        nombres = data['nombres']
        apellidos = data['apellidos']
        correo_electronico = data['correo_electronico']
        contrasena = data['contrasena']
        fecha_de_nacimiento = data['fecha_de_nacimiento']
        cedula_identidad = data['cedula_identidad']

        # Actualizar el usuario
        result = crud_usuarios.update_usuario(id_usuario, nombres, apellidos, correo_electronico, contrasena,
                                              fecha_de_nacimiento, cedula_identidad)

        return jsonify(result)

    except Exception as ex:
        # Manejar otros errores
        return jsonify({'error': str(ex)}), 500

    finally:
        # Cerrar la conexión
        db_helper.close()

# Endpoint para obtener todos los usuarios
@app.route('/api/usuarios', methods=['GET'])
def get_all_usuarios():
    try:
        # Conectar a la base de datos
        db_helper.connect()

        # Obtener todos los usuarios
        usuarios = crud_usuarios.read_all_usuarios()

        # Devolver los usuarios como JSON
        return jsonify(usuarios)

    except Exception as ex:
        # Manejar otros errores
        return jsonify({'error': str(ex)}), 500
    finally:
        # Cerrar la conexión
        db_helper.close()


# Endpoint para obtener un usuario por su ID
@app.route('/api/usuarios/<int:id_usuario>', methods=['GET'])
def get_usuario(id_usuario):
    try:
        # Conectar a la base de datos
        db_helper.connect()

        # Obtener el usuario por su ID
        usuario = crud_usuarios.get_usuario_by_id(id_usuario)

        if usuario:
            return jsonify(usuario)
        else:
            return jsonify({'message': 'Usuario no encontrado'}), 404  # Devolver 404 si no se encuentra el usuario

    except Exception as ex:
        # Manejar errores
        return jsonify({'error': str(ex)}), 500

    finally:
        # Cerrar la conexión
        db_helper.close()

# Endpoint para iniciar sesión
@app.route('/api/get_user_id', methods=['POST'])
def get_user_id():
    try:
        data = request.get_json()
        correo_electronico = data.get('correo_electronico')
        contrasena = data.get('contrasena')

        # Conectar a la base de datos y verificar las credenciales del usuario
        db_helper.connect()
        usuario = crud_usuarios.find_usuario_by_credentials(correo_electronico, contrasena)

        if usuario:
            # Si se encontró el usuario, devolver su ID en la respuesta
            return jsonify({'id_usuario': usuario['id_usuario']}), 200
        else:
            return jsonify({'error': 'Credenciales incorrectas'}), 401

    except Exception as ex:
        # Manejar otros errores
        return jsonify({'error': str(ex)}), 500

    finally:
        # Cerrar la conexión a la base de datos
        db_helper.close()


if __name__ == '__main__':
    # Iniciar el servidor Flask
    app.run(debug=True)
    CORS(app)