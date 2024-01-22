const inputs = document.querySelectorAll('input')
const verificarButton = document.getElementById('RestablecerContrasenia');
const inputNames = {}



inputs.forEach(input => {
    let nombre = (input.id == "ContraseniaUsuario") ? "Contraseña" : (input.id == "ContraseniaUsuario_confirm") ? "confirmar contraseña" : nombreInput(input.id)[0];
    inputNames[input.id] = nombre;
});


verificarButton.addEventListener('click', (evt) => {

    inputs.forEach(input => {
        let c_input = input.parentNode;
        let small = document.createElement('small');

        input.addEventListener('invalid', () => {
            small.classList.add('error');
            small.innerText = `El campo ${inputNames[input.id]} es requerido.`;

            c_input.appendChild(small);
        });

        input.addEventListener('input', () => {
            small.remove();
        });

    });


    validadContraseñas(evt);
});




function nombreInput(inputId) {
    let nombreInput = inputId.replace(/([a-z])([A-Z])/g, '$1 $2').split(' ');

    nombreInput = nombreInput.filter(function (palabra) {
        return palabra.length > 0;
    });

    return nombreInput;
}



function validadContraseñas(evt) {


    let contraseniaUsuario = document.getElementById("ContraseniaUsuario");
    let contraseniaUsuario_confirm = document.getElementById('ContraseniaUsuario_confirm');

    console.log(contraseniaUsuario.value !== contraseniaUsuario_confirm.value);
    if (contraseniaUsuario.value !== contraseniaUsuario_confirm.value) {


        evt.preventDefault();

        if(contraseniaUsuario_confirm.parentNode.querySelector('small')){
            let smallConfirm = contraseniaUsuario_confirm.parentNode.querySelector('small');
            smallConfirm.innerText = ""
        }


        let small = document.createElement('small');
        let c_input = contraseniaUsuario.parentNode
        
        small.classList.add('error', 'cu')
        small.innerText = "Las contraseñas no coinciden"

        c_input.append(small)

        contraseniaUsuario_confirm.value = ""
    }
}


function validarInputs() {
    inputs.forEach(input => {
        let c_input = input.parentNode;
        let b = document.createElement('small');

        input.addEventListener('invalid', () => {
            b.classList.add('error');

            if (input.type === 'email' && input.validity.typeMismatch) {
                b.innerText = 'introduce un correo electrónico válido.';
            } else {
                b.innerText = `El campo ${inputNames[input.id]} es requerido.`;
            }

            c_input.appendChild(b);
        });

        input.addEventListener('input', () => {
            b.remove();
        });
    });
}
