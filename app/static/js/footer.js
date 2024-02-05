const anios = document.querySelectorAll('span[data-id="anio"]');

anios.forEach((anio) => {
    anio.innerHTML = añoActual();
});

function añoActual() {
    let fechaActual = new Date();
    let anioActual = fechaActual.getFullYear();
    return anioActual;
}
