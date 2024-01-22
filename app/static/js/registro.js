const inputs = document.querySelectorAll("input");
const buttonRegistrar = document.getElementById("buttonRegistrar");
const verificarButton = document.getElementById("VerificarButton");
const forms = document.getElementById("Forms");
const backRegistro = document.getElementById("backRegistro");
const codigoUsuario = document.getElementById("CodigoUsuario");
const spanCorreo = document.getElementById("Correo");
const correoUsuario = document.getElementById("CorreoUsuario");
const inputNames = {};

inputs.forEach((input) => {
    let nombre =
        input.id == "ContraseniaUsuario"
            ? "contraseña"
            : input.id == "ContraseniaUsuario_confirm"
            ? "Confirmar contraseña"
            : nombreInput(input.id)[0];
    inputNames[input.id] = nombre;
});

buttonRegistrar.addEventListener("click", (evt) => {
    let inputsValidos = validarInputs();
    let contraseñasValidas = validadContraseñas();
    
    if (inputsValidos && contraseñasValidas) {
        delay = 2000;
        loader(delay);
    }
});

function nombreInput(inputId) {
    let nombreInput = inputId.replace(/([a-z])([A-Z])/g, "$1 $2").split(" ");

    nombreInput = nombreInput.filter(function (palabra) {
        return palabra.length > 0;
    });

    return nombreInput;
}

function validarInputs() {
    let hayInvalido = false;

    inputs.forEach((input) => {
        if (input.id !== "CodigoUsuario") {
            let c_input = input.parentNode;
            let b = document.createElement("small");

            input.addEventListener("invalid", () => {
                b.classList.add("error");

                if (input.type === "email" && input.validity.typeMismatch) {
                    b.innerText = "Introduce un correo electrónico válido.";
                } else {
                    b.innerText = `El campo ${
                        inputNames[input.id]
                    } es requerido.`;
                }

                c_input.appendChild(b);
                hayInvalido = true;
            });

            input.addEventListener("input", () => {
                b.remove();
            });
        }
    });

    return !hayInvalido;
}

function validadContraseñas() {
    let contraseniaUsuario = document.getElementById("ContraseniaUsuario");
    let contraseniaUsuario_confirm = document.getElementById(
        "ContraseniaUsuario_confirm"
    );

    if (contraseniaUsuario.value === "") {
        return false;
    }

    if (contraseniaUsuario.value !== contraseniaUsuario_confirm.value) {
        let small = document.createElement("small");
        let c_input = contraseniaUsuario.parentNode;

        small.classList.add("error", "cu");
        small.innerText = "Las contraseñas no coinciden";

        c_input.appendChild(small);

        contraseniaUsuario_confirm.value = "";
        return false;
    }

    return true;
}

verificarButton.addEventListener("click", () => {
    if (codigoUsuario.value === "") {
        let small = document.createElement("small");
        let c_input = codigoUsuario.parentNode;

        small.classList.add("error");
        small.innerText = "El codigo es requerido";

        c_input.appendChild(small);

        return;
    }
});

function loader(delay) {
    let c_loader = document.querySelector(".o_loader");
    c_loader.style.display = "block";

    setTimeout(() => {
        c_loader.style.display = "none";
    }, delay);
}
