const inputs = document.querySelectorAll("input");
const verificarButton = document.getElementById("VerificarButton");
const inputNames = {};

inputs.forEach((input) => {
    let nombre = nombreInput(input.id)[0];
    inputNames[input.id] = nombre;
});

verificarButton.addEventListener("click", () => {
    inputs.forEach((input) => {
        let c_input = input.parentNode;
        let small = document.createElement("small");

        input.addEventListener("invalid", () => {
            small.classList.add("error");
            small.innerText = `El campo ${inputNames[input.id]} es requerido.`;

            c_input.appendChild(small);
        });

        input.addEventListener("input", () => {
            small.remove();
        });
    });
});

function nombreInput(inputId) {
    let nombreInput = inputId.replace(/([a-z])([A-Z])/g, "$1 $2").split(" ");

    nombreInput = nombreInput.filter(function (palabra) {
        return palabra.length > 0;
    });

    return nombreInput;
}
