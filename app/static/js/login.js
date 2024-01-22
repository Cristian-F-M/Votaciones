const inputs = document.querySelectorAll('input');
const buttonSubmit = document.getElementById("buttonRegistrar");
const inputNames = {}

inputs.forEach(input => {
    let nombre = (input.id == "ContraseniaUsuario") ? "contraseña" : nombreInput(input.id)[0];
    inputNames[input.id] = nombre;
});


buttonSubmit.addEventListener("click", () => {
    // let lenNames = Object.keys(inputNames).length
    validarInputs();
    validadContraseñas();
});





function nombreInput(inputId) {
    let nombreInput = inputId.replace(/([a-z])([A-Z])/g, '$1 $2').split(' ');

    nombreInput = nombreInput.filter(function (palabra) {
        return palabra.length > 0;
    });

    return nombreInput;
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


function validadContraseñas(){
    let contraseniaUsuario = document.getElementById("ContraseniaUsuario");
    let contraseniaUsuario_confirm = document.getElementById('ContraseniaUsuario_confirm');

    if(contraseniaUsuario.value !== contraseniaUsuario_confirm.value){
        let small = document.createElement('small');
        let c_input = contraseniaUsuario.parentNode

        small.classList.add('error', 'cu')
        small.innerText = "Las contraseñas no coinciden"

        c_input.append(small)

        contraseniaUsuario_confirm.value = ""
    }


}