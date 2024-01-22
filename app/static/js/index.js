const anio = document.getElementById("anio");



anio.innerText = añoActual();

function añoActual() {
    let fechaActual = new Date();
    let anioActual = fechaActual.getFullYear();
    return anioActual;
}

