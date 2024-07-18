from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from models.models import Usuario, agregar_usuario, obtener_usuario_por_correo, existe_usuario
import pytesseract
from PIL import Image
import openai
from datetime import datetime, date

app = Flask(__name__, static_folder='static')
app.secret_key = 'Kvnsnt2210'

openai.api_key = "sk-proj-edvsqYDuJbHeuAm08p19T3BlbkFJk42lxoFCJbWnGFspEkdK"

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Configuración de la base de datos MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://usuario_bd:contraseña@localhost/nombre_bd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Rutas de Flask
@app.route('/')
def index():
    return render_template('Index.html')

@app.route('/crear-registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombres = request.form['txtNombres']
        apellidos = request.form['txtApellidos']
        correo_electronico = request.form['txtCorreo']
        contrasena = request.form['txtContrasena']
        fecha_de_nacimiento = request.form['txtFecha_de_nacimiento']
        cedula_identidad = request.form['txtCedula']

        if existe_usuario(correo_electronico):
            flash('El correo electrónico ya está registrado.', 'error')
        else:
            nuevo_usuario = Usuario(nombres, apellidos, correo_electronico, contrasena, fecha_de_nacimiento, cedula_identidad)
            agregar_usuario(nuevo_usuario)
            flash('Registro exitoso. Por favor inicie sesión.', 'success')
            return redirect(url_for('index'))

    return render_template('Index.html')

def calcular_edad(fecha_nacimiento):
    hoy = date.today()
    edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    return edad



@app.route('/inicio_sesion', methods=["GET","POST"])
def inicio_sesion():
    if request.method == 'POST':
        correo_electronico = request.form['txtCorreo']
        contrasena = request.form['txtContrasena']
        usuario = obtener_usuario_por_correo(correo_electronico)
        if usuario and usuario.verificar_contrasena(contrasena):
            session['usuario_logueado'] = usuario.correo_electronico
            return redirect(url_for('funcionamiento'))
        else:
            flash('Correo electrónico o contraseña incorrecta.', 'error')

    return redirect(url_for('index'))

@app.route('/funcionamiento')
def funcionamiento():
    if 'usuario_logueado' not in session:
        flash('Por favor, inicie sesión para ver esta página.', 'warning')
        return redirect(url_for('index'))
    correo_electronico = session['usuario_logueado']
    usuario = obtener_usuario_por_correo(correo_electronico)
    edad = calcular_edad(usuario.fecha_de_nacimiento)
    return render_template('funcionamiento.html', usuario=usuario, nombres = usuario.nombres, apellidos = usuario.apellidos, cedula_identidad = usuario.cedula_identidad, correo_electronico = usuario. correo_electronico, edad = edad)

@app.route('/principal')
def principal():
    return render_template('principal.html')

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        flash('No image uploaded', 'error')
        return redirect(url_for('index'))

    image = request.files['image']
    image = Image.open(image)

    # Extracción de texto utilizando Tesseract
    extracted_text = pytesseract.image_to_string(image)

    # Obtener texto adicional del formulario
    additional_text = request.form.get('additional_text', '')

    # Análisis del texto utilizando la nueva API de GPT-4
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Eres un asistente médico útil."},
            {"role": "user", "content": f"Brindar posibles recomendaciones precisas basadas en el siguiente texto extraído de una imagen médica: {extracted_text} y la información adicional: {additional_text}"}
        ],
        max_tokens=500
    )

    analysis = response.choices[0].message['content'].strip()

    return render_template('perfil.html',  extracted_text=extracted_text, additional_text=additional_text, analysis=analysis)



if __name__ == '__main__':
    app.run(debug=True)
