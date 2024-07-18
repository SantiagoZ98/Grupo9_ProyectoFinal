from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, make_response
from flask_weasyprint import HTML, render_pdf
from models.models import Usuario, agregar_usuario, obtener_usuario_por_correo, existe_usuario

import openai


app = Flask(__name__, static_folder='static')
app.secret_key = 'tu_clave_secreta_aqui'

@app.route('/')
def index():
   
    return render_template('Index.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombres_completos']
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        if existe_usuario(correo):
            flash('Su correo electronico ya se encuentra registrado.', 'error')
        else:
            nuevo_usuario = Usuario(nombre, correo, contraseña)
            agregar_usuario(nuevo_usuario)
            flash('Registro exitoso. Por favor inicie sesión.', 'success')
        return redirect(url_for('index'))
    return render_template('Index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        usuario = obtener_usuario_por_correo(correo)
        if usuario and usuario.verificar_contraseña(contraseña):
            session['usuario_logueado'] = usuario.correo
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
    usuario = obtener_usuario_por_correo(correo)
    return render_template('funcionamiento.html', usuario=usuario)

@app.route('/principal')
def principal():
    return render_template('principal.html')



@app.route('/perfil')
def perfil():
    return render_template('perfil.html')

@app.route('/descargar_resultados')
def descargar_resultados():
    # Asegúrate de que el usuario esté logueado
    if 'usuario_logueado' not in session:
        flash('Por favor, inicie sesión para acceder a esta funcionalidad.', 'warning')
        return redirect(url_for('index'))

    # Función para construir el prompt basado en la etiqueta
    def construir_prompt(etiqueta, texto_usuario):
        if etiqueta == "img1":
            descripcion = "Si ves una mariposa o un murciélago, indica..."
        elif etiqueta == "img2":
            descripcion = "Ver dos figuras humanas sugiere..."
        # Continúa para las demás etiquetas
        else:
            descripcion = "Interpretación general."
        
        return f"Interpretar la respuesta '{texto_usuario}' para la imagen {etiqueta}: {descripcion}"


    # Función para generar el diagnóstico con OpenAI
    def generar_diagnostico(texto_prompt):
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=texto_prompt,
            temperature=0.7,
            max_tokens=150,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        return response.choices[0].text.strip()




if __name__ == '__main__':
    app.run(debug=True)
