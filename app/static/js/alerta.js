const c_mensajes = document.querySelector(".c_mensajes");

document.addEventListener("DOMContentLoaded", () => {
    iniciarAnimaciones();
});

async function iniciarAnimaciones() {
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
                    c_mensajes.style.display = "none";
                }, 500);
            });
        });
    });
}

function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}
