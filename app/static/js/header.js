const btnMenu = document.getElementById("btn_menu");
const menu_lateral = document.getElementById("menu-lateral");
const header = document.getElementById("header");
const links = document.querySelectorAll("a");
const candidatos = document.getElementById("Candidatos");
const c_addCandidato = document.querySelector(".c_addCandidato");
const o_crearCandidato = document.querySelector(".o_crearCandidato");
const btnsCerrar = document.querySelectorAll("#BTNCerrar");
const documentoAprendiz = document.getElementById("DocumentoAprendiz");
const tags = document.querySelectorAll(".tag");
const btnAceptar = document.getElementById("BTNAceptar");
const formAgragarCandidato = document.getElementById("FormAgragarCandidato");
const buscarAprendiz = document.getElementById("BuscarAprendiz");
const c_loading = document.querySelector(".c_loading");
const tag_rol = document.querySelector(".tag.rol");
const tag_foto = document.querySelector(".tag.foto");
const tag_descripcion = document.querySelector(".tag.descripcion");
const tag_estado = document.querySelector(".tag.estado");
const nombreAprendiz = document.getElementById("NombreAprendiz");
const valido = document.getElementById("Valido");
const divInformacionAprendiz = document.getElementById("InformacionAprendiz");

btnMenu.addEventListener("click", () => {
    if (!btnMenu.hasAttribute("active")) {
        btnMenu.setAttribute("active", "");
    } else {
        btnMenu.removeAttribute("active");
    }

    if (menu_lateral.hasAttribute("visible")) {
        menu_lateral.removeAttribute("visible");
    } else {
        menu_lateral.setAttribute("visible", "");
    }
});

colorHeader();

window.addEventListener("scroll", colorHeader);

links.forEach((link) => {
    link.addEventListener("click", () => {
        if (btnMenu.hasAttribute("active")) {
            btnMenu.removeAttribute("active");
        }

        if (menu_lateral.hasAttribute("visible")) {
            menu_lateral.removeAttribute("visible");
        }
    });
});

var scrollSize = scrollSize;

function colorHeader() {
    if (window.scrollY > scrollSize) {
        header.style.backgroundColor =
            "#262"; /* Vuelve a azul si estás arriba de los 100 píxeles */
    } else {
        header.style.backgroundColor =
            "#0608"; /* Cambia a rojo después de desplazar 100 píxeles */
    }
}

candidatos.addEventListener("click", (evt) => {
    evt.preventDefault();
    o_crearCandidato.setAttribute("show", true);
    c_addCandidato.setAttribute("show", true);
});

btnsCerrar.forEach((btnCerrar) => {
    btnCerrar.addEventListener("click", (evt) => {
        evt.preventDefault();
        c_addCandidato.removeAttribute("show");
        resetAgregarCandidato();
        setTimeout(() => {
            o_crearCandidato.removeAttribute("show");
        }, 120);
    });
});

function resetAgregarCandidato() {
    tags.forEach((tag) => {
        tag.className = "";
        tag.classList.add("tag");
    });
    divInformacionAprendiz.removeAttribute("show");
    btnAceptar.disabled = true;
}

let buscando = false; // Variable para rastrear si se está realizando una búsqueda

buscarAprendiz.addEventListener("click", async () => {
    c_loading.setAttribute("show", "");
    buscarAprendiz.style.cursor = "wait";
    divInformacionAprendiz.removeAttribute("show");

    if (buscando) {
        return;
    }

    buscando = true;

    try {
        let data = {
            documentoUsuario: documentoAprendiz.value,
        };

        var rs = await informacionAprendiz(data);
    } catch (error) {
        // console.error("Error en la petición:", error);
        // crearAlerta("Ocurrió un error al procesar la solicitud", true);
    } finally {
        setTimeout(() => {
            buscando = false;
            buscarAprendiz.disabled = false;
            if (rs.rs == 404) {
                crearAlerta("No se encuentra el aprendiz", true);
            }
            c_loading.removeAttribute("show");
            buscarAprendiz.style.cursor = "";

            if (rs.rs == 304) {
                llenarDatosAprendiz(rs.usuario);
            }
        }, 3000);
    }
});

async function informacionAprendiz(data) {
    let response = await fetch("/Buscar-aprendiz", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });
    let json = await response.json();
    return json;
}

function llenarDatosAprendiz(usuario) {
    documentoAprendiz.value = "";
    formAgragarCandidato.action = `/Agregar-candidato/${usuario.idUsuario}`;
    nombreAprendiz.innerText = usuario.nombreUsuario;
    valido.classList.add(usuario.usuarioValido ? "valida" : "invalida");
    valido.innerText = usuario.usuarioValido ? "valido" : "invalido";
    tag_rol.innerText = usuario.rolUsuario;
    tag_rol.classList.add("valida");
    tag_foto.classList.add(usuario.fotoUsuario ? "valida" : "invalida");
    tag_descripcion.classList.add(
        usuario.descripcionUsuario ? "valida" : "invalida"
    );

    tag_estado.innerText = usuario.estadoUsuario;
    tag_estado.classList.add(usuario.estadoUsuarioV ? "valida" : "invalida");
    
    if (usuario.usuarioValido) {
        btnAceptar.disabled = false;
    }

    divInformacionAprendiz.setAttribute("show", "");
}
