const lis = document.querySelectorAll(".c_menu-contenedores ul li");
const contenedores = document.querySelectorAll(".contenedores .contenedor");
const btnscerrar = document.querySelectorAll('[data-name="cerrar"]');
const as = document.querySelectorAll("table tbody tr td a");

///////////////////////////////////////////////////////////////////////////////////////////////
lis.forEach((li) => {
    let contenido = document.querySelector(
        `.contenedores .contenedor[data-name='${li.getAttribute("data-name")}']`
    );

    li.addEventListener("click", () => {
        lis.forEach((li) => {
            li.removeAttribute("active");
        });

        contenedores.forEach((contenedor) => {
            contenedor.removeAttribute("show");
        });

        li.setAttribute("active", "");
        contenido.setAttribute("show", "");
    });
});

///////////////////////////////////////////////////////////////////////////////////////////////

btnscerrar.forEach((i) => {
    let overlay = i.parentNode.parentNode.parentNode.parentNode;

    i.addEventListener("click", (evt) => {
        evt.stopPropagation();

        overlay.removeAttribute("show");
        console.log(overlay);
    });
});

as.forEach((a) => {
    a.addEventListener("click", () => {
        console.log("hola");
        let overlay = a.querySelector(".overlay-editar");

        overlay.setAttribute("show", "");
    });
});

scrollSize = -1;
