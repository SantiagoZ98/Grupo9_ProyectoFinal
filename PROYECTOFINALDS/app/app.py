from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, make_response
from Usuarios_grupo9.conexion.unionDB import DBHelper
from Usuarios_grupo9.CRUDS.crudUsers import CRUDOperations
import bcrypt
from flask_jwt_extended import create_access_token, JWTManager
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
app.secret_key = 'Kszs2298'
app.config['JWT_SECRET_KEY'] = 'Kvnsnt2210'
CORS(app, origins='http://localhost:3000')
jwt = JWTManager(app)

# Configuración de la base de datos
db_helper = DBHelper(host='localhost', database='crud_usuarios', user='root', password='adminkvn-12345')
crud_usuarios = CRUDOperations(db_helper)

@app.route('/')
def index():
    return render_template('Index.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombres_completos']
        correo = request.form['correo']
        contrasena = request.form['contraseña']
        if crud_usuarios.existe_usuario(correo):
            flash('El correo electrónico ya está registrado.', 'error')
        else:
            contrasena_hash = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())
            nuevo_usuario = {
                'nombre': nombre,
                'correo': correo,
                'contrasena': contrasena_hash.decode('utf-8')
            }
            crud_usuarios.agregar_usuario(nuevo_usuario)
            flash('Registro exitoso. Por favor inicie sesión.', 'success')
        return redirect(url_for('index'))
    return render_template('Index.html')

@app.route('/inicio_sesion', methods=['GET', 'POST'])
def inicio_sesion():
    if request.method == 'POST':
        correo = request.form['correo']
        contrasena = request.form['contraseña']
        usuario = crud_usuarios.obtener_usuario_por_correo(correo)
        if usuario and bcrypt.checkpw(contrasena.encode('utf-8'), usuario['contrasena'].encode('utf-8')):
            session['usuario_logueado'] = usuario['correo']
            return redirect(url_for('funcionamiento'))
        else:
            flash('Correo electrónico o contraseña incorrecta.', 'error')
            return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route('/funcionamiento')
def funcionamiento():
    if 'usuario_logueado' not in session:
        flash('Por favor, inicie sesión para ver esta página.', 'warning')
        return redirect(url_for('index'))
    correo = session['usuario_logueado']
    usuario = crud_usuarios.obtener_usuario_por_correo(correo)
    return render_template('funcionamiento.html', usuario=usuario)

@app.route('/principal')
def principal():
    return render_template('principal.html')

@app.route('/guardar_respuesta', methods=['POST'])
def guardar_respuesta():
    data = request.get_json()
    texto = data['texto']
    imagen_actual = data['imagen_actual']
    db_helper.connect()
    db_helper.execute("INSERT INTO respuestas (etiqueta, texto) VALUES (%s, %s)", (imagen_actual, texto))
    db_helper.close()
    return jsonify({"mensaje": "Guardado exitosamente"})

@app.route('/perfil')
def perfil():
    return render_template('perfil.html')

@app.route('/descargar_resultados')
def descargar_resultados():
    if 'usuario_logueado' not in session:
        flash('Por favor, inicie sesión para acceder a esta funcionalidad.', 'warning')
        return redirect(url_for('index'))

    def construir_prompt(etiqueta, texto_usuario):
        if etiqueta == "img1":
            descripcion = "Si ves una mariposa o un murciélago, indica..."
        elif etiqueta == "img2":
            descripcion = "Ver dos figuras humanas sugiere..."
        else:
            descripcion = "Interpretación general."
        return f"Interpretar la respuesta '{texto_usuario}' para la imagen {etiqueta}: {descripcion}"

    db_helper.connect()
    respuestas = db_helper.fetch_all("SELECT etiqueta, texto FROM respuestas")
    db_helper.close()
    
    diagnosticos = []
    for respuesta in respuestas:
        etiqueta, texto_usuario = respuesta
        prompt = construir_prompt(etiqueta, texto_usuario)
        diagnostico = "Genera tu diagnóstico aquí basado en el prompt"  # Simula la respuesta del diagnóstico
        diagnosticos.append((etiqueta, diagnostico))

    html = render_template('resultados_pdf.html', diagnosticos=diagnosticos)
    return render_pdf(HTML(string=html))

if __name__ == '__main__':
    app.run(debug=True)
