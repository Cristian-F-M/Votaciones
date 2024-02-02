const inputsCheckBox = document.querySelectorAll('input[type="checkbox"]');
const BTNVer = document.querySelectorAll("#Ver");

scrollSize = 0

inputsCheckBox.forEach((input) => {
    let label = document.querySelector(`label[for="${input.id}"]`);

    estiloInputs(input, label);

    input.addEventListener("change", () => {});
});

function estiloInputs(input, label) {
    // let estado = label.getAttributte('estado')
    // if (estado === 'activo') {
    //     label.setAttribute('selected', true)
    // }
    // if (!input.checked) {
    //     label.setAttribute('selected', false)
    // }
}

BTNVer.forEach((ver) => {
    let data_id = ver.getAttribute("data-id");
    let o_informacion_votacion = document.querySelector(
        `.o_informacion-votacion[data-id="${data_id}"]`
    );
    let informacion_votacion = o_informacion_votacion.querySelector(
        ".informacion-votacion"
    );
    let cerrar = informacion_votacion.querySelector(".cerrar>i");

    ver.addEventListener("click", (evt) => {
        evt.preventDefault();
        showInformacionVotacion(o_informacion_votacion, informacion_votacion);
    });

    cerrar.addEventListener("click", (evt) => {
        evt.preventDefault();
        hideInformacionVotacion(o_informacion_votacion, informacion_votacion);
    });
});

function showInformacionVotacion(overlay, informacion) {
    overlay.setAttribute("show", "");
    setTimeout(() => {
        informacion.setAttribute("show", "");
    }, 20);
}

function hideInformacionVotacion(overlay, informacion) {
    informacion.removeAttribute("show");
    setTimeout(() => {
        overlay.removeAttribute("show");
    }, 300);
}
