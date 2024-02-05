const anio = document.getElementById("anio");
const drops = document.querySelectorAll(".drop-down");
const EnviarCorreo = document.getElementById("EnviarCorreo");
const main = document.querySelector("main");

scrollSize = 250;

anio.innerText = añoActual();

function añoActual() {
    let fechaActual = new Date();
    let anioActual = fechaActual.getFullYear();
    return anioActual;
}

drops.forEach((drop) => {
    let cTitulo = drop.querySelector(".c_titulo");
    let contendo = drop.querySelector(".c_contenido");
    let i = cTitulo.querySelector("i");

    cTitulo.addEventListener("click", () => {
        contendo.classList.toggle("show");
        i.classList.toggle("subir");
    });
});

EnviarCorreo.addEventListener("click", () => {
    let inputs = document.querySelectorAll("input, textarea");

    let todosLosCamposValidos = true;
    inputs.forEach(function (input) {
        if (!input.checkValidity()) {
            todosLosCamposValidos = false;
        }
    });

    if (todosLosCamposValidos) {
        data = {
            nombre: Nombre.value,
            correo: Correo.value,
            mensaje: Mensaje.value,
        };

        Nombre.value = "";
        Correo.value = "";
        Mensaje.value = "";

        enviarSugerencia(data);
    } else {
        crearAlerta("Algunos campos no esta completos", true);
    }
});

function enviarSugerencia(data) {
    fetch("/Enviar-sugerencias", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    })
        .then((response) => response.text())
        .then((texto) => {
            console.log("Respuesta del servidor:", texto);

            crearAlerta(texto);
        })
        .catch((error) => {
            console.error("Error en la petición:", error);
            crearAlerta("Ocurio un error al procesar la solicitud", true);
        });
}

function crearAlerta(mensaje, error = false) {
    if (main.querySelector(".c_mensajes")) {
        main.removeChild(main.querySelector(".c_mensajes"));
    }

    let divMensajes = document.createElement("div");
    let divMensaje = document.createElement("div");
    let p = document.createElement("p");
    let divCarga = document.createElement("div");

    divMensajes.classList.add("c_mensajes");
    divMensajes.setAttribute("id", "Mensajes");
    divMensajes.id = "Mensajes";
    divMensaje.classList.add("mensaje");
    if (error) {
        divMensaje.classList.add("text-error");
    }
    divCarga.classList.add("c_carga");
    p.innerText = mensaje;

    divMensaje.append(p);
    divMensaje.append(divCarga);
    divMensajes.append(divMensaje);
    main.append(divMensajes);

    iniciarAnimaciones(divMensajes);
}
