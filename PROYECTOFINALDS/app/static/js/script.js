const btnSingIn = document.getElementById("sing-in"),
      btnSingUp = document.getElementById("sing-up"),
      formRegister = document.querySelector(".register"),
      formLogin = document.querySelector(".login");

btnSingIn.addEventListener("click", e => {
    formRegister.classList.add("hide");
    formLogin.classList.remove("hide");
});

btnSingUp.addEventListener("click", e => {
    formLogin.classList.add("hide");
    formRegister.classList.remove("hide");
});

// Agregar manejador de eventos para el envío del formulario de registro
document.getElementById('register-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const nombres = document.querySelector('input[name="nombres"]').value;
    const apellidos = document.querySelector('input[name="apellidos"]').value;
    const correo_electronico = document.querySelector('input[name="correo_electronico"]').value;
    const contrasena = document.querySelector('input[name="contrasena"]').value;
    const fecha_de_nacimiento = document.querySelector('input[name="fecha_de_nacimiento"]').value;
    const cedula_identidad = document.querySelector('input[name="cedula_identidad"]').value;

    const data = {
        nombres,
        apellidos,
        correo_electronico,
        contrasena,
        fecha_de_nacimiento,
        cedula_identidad
    };

    try {
        const response = await fetch('http://127.0.0.1:5000/api/usuarios', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error('Error al crear el usuario');
        }

        const result = await response.json();
        console.log('Usuario creado:', result);
    } catch (error) {
        console.error('Error:', error);
    }
});

