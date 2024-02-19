const tdsUsuario = document.querySelectorAll("tbody tr td:first-child");
const trSanciones = document.querySelectorAll("tbody tr");
const tbody = document.querySelector("tbody");
const o_buscarUsuario = document.getElementById("O_buscarUsuario");
const cerrarbuscarUsuario = document.getElementById("CerrarbuscarUsuario");
const btnBuscarUsuario = document.getElementById("BTNBuscarUsuario");
const documentoUsuario = document.getElementById("DocumentoUsuarioBuscar");
const buscarUsuario = document.getElementById("BuscarUsuario");
const cerrarInformacionAprendiz = document.querySelectorAll(
    '[data-name="cerrar-informacion-aprendiz"]'
);

tdsUsuario.forEach((td) => {
    td.addEventListener("click", () => {
        let dataId = td.getAttribute("data-id");
        let o_informacionUsuarioSancion = document.querySelector(
            `.o_informacion-aprendiz-sancion[data-id='${dataId}']`
        );

        o_informacionUsuarioSancion.setAttribute("show", "");
    });
});

cerrarInformacionAprendiz.forEach((cerrar) => {
    cerrar.addEventListener("click", () => {
        let dataId = cerrar.getAttribute("data-id");
        let o_informacionUsuarioSancion = document.querySelector(
            `.o_informacion-aprendiz-sancion[data-id='${dataId}']`
        );

        o_informacionUsuarioSancion.removeAttribute("show");
    });
});

btnBuscarUsuario.addEventListener("click", () => {
    o_buscarUsuario.setAttribute("show", "");
});

cerrarbuscarUsuario.addEventListener("click", () => {
    o_buscarUsuario.removeAttribute("show", "");
});

buscarUsuario.addEventListener("click", async () => {
    data = {
        documentoUsuario: documentoUsuario.value,
    };

    rs = await buscarSancionesUsuario(data);

    if (rs.rs == 404) {
        if (rs.rz == "usuario") {
            crearAlerta("No se encuentra el usuario", true);
        }

        if (rs.rz == "sancion") {
            crearAlerta("El usuario no tiene sanciones");
            restablecerBuscarUsuario();
        }
    }

    if (rs.rs == 200) {
        restablecerBuscarUsuario();

        let sanciones = rs.sanciones;

        // var sancionesCoincidentes = [];
        // var sancionesNoCoincidentes = [];

        sancionesCoincidentes = añadirTrCoincidiente(sanciones);
        sancionesNoCoincidentes = añadirTrNoCoincidiente(
            sanciones,
            sancionesCoincidentes
        );

        tbody.innerHTML = "";

        sancionesCoincidentes.forEach((tr) => {
            tbody.appendChild(tr);
        });

        tr = crearTr("Otras sanciones");

        tbody.appendChild(tr);

        sancionesNoCoincidentes.forEach((tr) => {
            tbody.appendChild(tr);
        });

        o_buscarUsuario.removeAttribute("show", "");
    }
});

async function buscarSancionesUsuario(data) {
    let response = await fetch("/buscar/sanciones", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });
    let json = await response.json();
    return json;
}

function restablecerBuscarUsuario() {
    documentoUsuario.value = "";
    // o_buscarUsuario.removeAttribute("show");
}

function añadirTrNoCoincidiente(sanciones, sancionesCoincidentes) {
    let sancionesNoCoincidentes = [];

    trSanciones.forEach((tr) => {
        sanciones.forEach((sancion) => {
            if (!(tr.getAttribute("data-id") == sancion.idSancion)) {
                if (!sancionesCoincidentes.some((item) => item === tr)) {
                    if (!sancionesNoCoincidentes.some((item) => item === tr)) {
                        sancionesNoCoincidentes.push(tr);
                    }
                }
            }
        });
    });

    return sancionesNoCoincidentes;
}
function añadirTrCoincidiente(sanciones) {
    let sancionesCoincidentes = [];
    trSanciones.forEach((tr) => {
        sanciones.forEach((sancion) => {
            if (tr.getAttribute("data-id") == sancion.idSancion) {
                sancionesCoincidentes.push(tr);
            }
        });
    });
    return sancionesCoincidentes;
}

function crearTr(txt) {
    let tr = document.createElement("tr");

    for (let i = 0; i < 4; i++) {
        let td = document.createElement("td");
        td.style.fontSize = '20px'
        td.style.backgroundColor = '#fff'
        if (i == 2) {
            td.innerText = txt;
        }
        tr.appendChild(td);
    }

    // td.setAttribute("colspan", "4");

    return tr;
}
