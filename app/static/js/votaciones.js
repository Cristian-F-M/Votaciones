const inputsCheckBox = document.querySelectorAll('input[type="checkbox"]');
const BTNVer = document.querySelectorAll("#Ver");
const oNuevaVotacion = document.getElementById("ONuevaVotacion");
const btnNuevaVotacion = document.getElementById("BTNNuevaVotacion");
const cerrarNuevaVotacion = document.getElementById("CerrarNuevaVotacion");
const nuevaVotacion = document.getElementById("NuevaVotacion");
const fechaInicio = document.getElementById("FechaInicio");
const eliminarVotacion = document.querySelectorAll("#EliminarVotacion");
const trHead = document.getElementById("TrHead");
const table = document.querySelector(".table");

scrollSize = 0;

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

btnNuevaVotacion.addEventListener("click", () => {
    fechaInicio.value = new Date(Date.now()).toISOString().substring(0, 10);

    oNuevaVotacion.setAttribute("show", true);
    setTimeout(() => {
        nuevaVotacion.setAttribute("show", true);
    }, 30);
});

cerrarNuevaVotacion.addEventListener("click", () => {
    fechaInicio.value = "";
    nuevaVotacion.setAttribute("show", false);
    setTimeout(() => {
        oNuevaVotacion.setAttribute("show", false);
    }, 80);
});

eliminarVotacion.forEach((btn) => {
    let form = document.querySelector(
        `form[data-id='${btn.getAttribute("data-id")}']`
    );

    btn.addEventListener("click", () => {
        form.submit();
    });
});

table.addEventListener("scroll", colorHeader);

var scrollSizeTbody = 10;

function colorHeader() {
    let ths = trHead.querySelectorAll("th");
    let lastTh = trHead.querySelector("th:last-child");
    let colorFondo = table.scrollTop > scrollSizeTbody ? "#7aad7a" : "#2729";

    ths.forEach((th) => {
        th.style.backgroundColor = colorFondo;
    });

    if (table.scrollTop < scrollSizeTbody) {
        lastTh.style.backgroundColor = "transparent";
    } else {
        lastTh.style.backgroundColor = colorFondo;
    }
}
