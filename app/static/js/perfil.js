const fotoUsuario = document.getElementById("imgFotoUsuario");
const inputFile = document.getElementById("FotoUsuario");
const OverlayFoto = document.getElementById("Overlay-foto");
const NombreArchivo = document.getElementById("Nombre-archivo");
const BTNEditar = document.getElementById("EditarPerfil");
const acciones = document.getElementById("Acciones");
const contraseniaOld = document.getElementById("ContraseniaOld");
const nuevaContrasenia = document.getElementById("NuevaContrasenia");
const inputCambiarContrasenia = acciones.querySelector("input");
const BTNActualizar = document.getElementById("BTNActualizar");
const inputs = document.querySelectorAll("input");
const textareas = document.querySelectorAll("textarea");

fotoUsuario.addEventListener("click", () => {
    inputFile.showPicker();
});

scrollSize = 20


OverlayFoto.addEventListener("click", () => {
    inputFile.showPicker();
});

inputFile.addEventListener("change", handleFileChange);

BTNEditar.addEventListener("click", handleEditarClick);

inputCambiarContrasenia.addEventListener(
    "change",
    handleCambiarContraseniaChange
);

function handleCambiarContraseniaChange() {
    showAcciones();

    if (inputCambiarContrasenia.checked) {
        setEditableAttribute([contraseniaOld, nuevaContrasenia], true);
    } else {
        setEditableAttribute([contraseniaOld, nuevaContrasenia], false);
    }
}

function habilitarInputs() {
    setDisabledAttribute([...inputs, ...textareas], false);
}

function deshabilitarInputs() {
    setDisabledAttribute([...inputs, ...textareas], true);
}

function handleFileChange(evt) {
    let file = evt.target.files[0];
    if (file) {
        fotoUsuario.src = URL.createObjectURL(file);
        fotoUsuario.alt = file.name;
        NombreArchivo.innerHTML = file.name;
    }
}

function handleEditarClick() {
    let editar = acciones.getAttribute("editar");
    let actualizar = BTNActualizar.getAttribute("editar");

    if (editar === "false" && actualizar === "false") {
        setEditableAttribute([acciones, BTNActualizar], true);
        habilitarInputs();
        crearAlerta("Se habilito el editar perfil")
    } else {
        setEditableAttribute([acciones, BTNActualizar], false);
        inputCambiarContrasenia.checked = false;
        showAcciones();
        deshabilitarInputs();
        crearAlerta("Se deshabilito el editar perfil")
    }
}

function setEditableAttribute(elements, value) {
    elements.forEach((element) => {
        element.setAttribute("editar", value.toString());
    });
}

function setDisabledAttribute(elements, value) {
    elements.forEach((element) => {
        if (
            element !== nuevaContrasenia.querySelector("input") &&
            element !== contraseniaOld.querySelector("input")
        ) {
            element.disabled = value;
        }
    });
}

function showAcciones() {
    let editar = inputCambiarContrasenia.checked ? true : false;

    console.log(`editar ${!editar}`);

    
    contraseniaOld.querySelector("input").disabled = !editar;
    nuevaContrasenia.querySelector("input").disabled = !editar;

    contraseniaOld.setAttribute("editar", editar);
    nuevaContrasenia.setAttribute("editar", editar);
}
