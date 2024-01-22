const inputs = document.querySelectorAll("input");
const BTNVotar = document.getElementById("BTNVotar");
const main = document.querySelector("main");

BTNVotar && BTNVotar.addEventListener("click", (evt) => {
    rs = validarVoto();

    if (!rs) {
        evt.preventDefault();

        if(main.querySelector('.c_mensajes')){
            main.removeChild(main.querySelector('.c_mensajes'))
        }



        let divMensajes = document.createElement("div");
        let divMensaje = document.createElement("div");
        let p = document.createElement("p");
        let divCarga = document.createElement("div");

        divMensajes.classList.add("c_mensajes");
        divMensaje.classList.add("mensaje");
        divMensaje.classList.add("text-error");
        divCarga.classList.add("c_carga");
        p.innerText = "Seleccióna un candidato o Voto en blanco";

        divMensaje.append(p);
        divMensaje.append(divCarga);
        divMensajes.append(divMensaje);
        main.append(divMensajes);

        iniciarAnimaciones();
    }
});

inputs.forEach((input) => {
    input.addEventListener("click", () => {
        resetInputs();
        let label = document.querySelector(`label[for='${input.id}']`);
        if (label.getAttribute("seleccionado") === "false") {
            label.setAttribute("seleccionado", "true");
        }
    });
});

function resetInputs() {
    inputs.forEach((input) => {
        let label = document.querySelector(`label[for='${input.id}']`);

        if (label.getAttribute("seleccionado") === "true") {
            label.setAttribute("seleccionado", "false");
        }
    });
}

function validarVoto() {
    let rs = false;

    forEach: for (let i = 0; i < inputs.length; i++) {
        if (inputs[i].checked) {
            rs = true;
            break forEach;
        }
    }

    return rs;
}
