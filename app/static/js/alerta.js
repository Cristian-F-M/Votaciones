const c_mensajes = document.getElementById("Mensajes");

document.addEventListener("DOMContentLoaded", () => {
    iniciarAnimaciones();
});

async function iniciarAnimaciones(mss) {
    let mensajes = document.querySelectorAll(".mensaje");

    mensajes.forEach(async (mensaje, index) => {
        mensaje.style.zIndex = mensajes.length - index;

        delay = index * 400;
        mensaje.style.animationDelay = `${delay}ms`;

        let carga = mensaje.querySelector(".c_carga");

        mensaje.setAttribute("animacion", "in");

        mensaje.addEventListener("animationend", function (evt) {
            if (evt.animationName === "mensajeInDesktop") {
                carga.setAttribute("animacion", "true");

                carga.addEventListener("animationend", () => {
                    mensaje.style.animationDelay = `0ms`;
                    mensaje.setAttribute("animacion", "out");
                });
            }

            if (evt.animationName === "mensajeInMovil") {
                let delay = index * 1.5;

                carga.style.animationDelay = `${delay}s`;

                carga.setAttribute("animacion", "true");

                carga.addEventListener("animationend", () => {
                    mensaje.style.animationDelay = `0ms`;
                    mensaje.setAttribute("animacion", "out");
                });
            }

            mensaje.addEventListener("animationend", () => {
                setTimeout(() => {
                    if (c_mensajes) {
                        c_mensajes.style.display = "none";
                    }

                    if (mss) {
                        mss.style.display = "none";
                    }
                }, 500);
            });
        });
    });
}

function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}

function crearAlerta(msg, error = false) {
    let main = document.querySelector("main");
    if (main.querySelector(".c_mensajes")) {
        main.removeChild(main.querySelector(".c_mensajes"));
    }

    let divMensajes = document.createElement("div");
    let divMensaje = document.createElement("div");
    let p = document.createElement("p");
    let divCarga = document.createElement("div");

    divMensajes.classList.add("c_mensajes");
    divMensaje.classList.add("mensaje");
    if (error) {
        divMensaje.classList.add("text-error");
    }
    divCarga.classList.add("c_carga");
    p.innerText = msg;

    divMensaje.append(p);
    divMensaje.append(divCarga);
    divMensajes.append(divMensaje);
    main.append(divMensajes);

    iniciarAnimaciones(divMensajes);
}
