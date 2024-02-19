const trsBody = document.querySelectorAll("tbody tr");
const o_buscarUsuario = document.getElementById("O_buscarUsuario");
const cerrarbuscarUsuario = document.getElementById("CerrarbuscarUsuario");
const btnBuscarUsuario = document.getElementById("BTNBuscarUsuario");
const documentoUsuario = document.getElementById("DocumentoUsuarioBuscar");
const buscarUsuario = document.getElementById("BuscarUsuario");
const cerrarEditarUsuario = document.querySelectorAll(
    '[data-name="cerrarEditarUsuario"]'
);

trsBody.forEach((tr) => {
    tr.addEventListener("click", () => {
        let dataId = tr.getAttribute("data-id");
        let o_editarUsuario = document.querySelector(
            `.o_editarUsuario[data-id='${dataId}']`
        );

        o_editarUsuario.setAttribute("show", "");
    });
});

cerrarEditarUsuario.forEach((cerrar) => {
    cerrar.addEventListener("click", () => {
        let dataId = cerrar.getAttribute("data-id");
        let o_editarUsuario = document.querySelector(
            `.o_editarUsuario[data-id='${dataId}']`
        );

        o_editarUsuario.removeAttribute("show", "");
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

    rs = await informacionUsuario(data);

    if (rs.rs == 404) {
        crearAlerta("No se encuentra el usuario", true);
    }

    if (rs.rs == 200) {
        restablecerBuscarUsuario();

        let o_editarUsuario = document.querySelector(
            `.o_editarUsuario[data-id='${rs.idUsuario}']`
        );

        o_editarUsuario.setAttribute("show", "");
    }
});

async function informacionUsuario(data) {
    let response = await fetch("/search/user", {
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

    o_buscarUsuario.removeAttribute("show");
}
