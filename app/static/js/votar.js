const inputs = document.querySelectorAll("input");
const BTNVotar = document.getElementById("BTNVotar");
const main = document.querySelector("main");
const cards = document.querySelectorAll('#card-candidato');
const imgCandidatos = document.querySelectorAll('.c_foto-candidato');
const nombreCandidato = document.querySelectorAll('.c_nombre-candidato>h3');
scrollSize = 10

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



imgCandidatos.forEach((img) => {

    let card = img.parentNode;
    let c_card = card.parentNode;
    let c_info = c_card.querySelector('.c_informacion-candidato')
    let info = c_info.querySelector('.informacion-candidato')
    let cerrar = info.querySelector('.cerrar>i')
    let bCerrar = info.querySelector('.c_button>button')
    let body = document.body;

    img.addEventListener('click', () => {
        document.querySelector('main').style.overflow = 'hidden';
        body.style.overflowY = 'hidden';
        showInfo(c_info, info)
    });

    bCerrar.addEventListener('click', (evt) => {
        evt.preventDefault();
        hideInfo(c_info, info)
        body.style.overflowY = 'auto';
    })
    cerrar.addEventListener('click', (evt) => {
        evt.preventDefault();
        hideInfo(c_info, info)
        body.style.overflowY = 'auto';
    })


});



function showInfo(c_info, info) {
    c_info.setAttribute('open', '')
    setTimeout(() => {
        info.setAttribute('open', '');
    }, 20);
}

function hideInfo(c_info, info) {
    info.removeAttribute('open');
    setTimeout(() => {
        c_info.removeAttribute('open')
    }, 300);
}