const btnMenu = document.getElementById("btn_menu");
const menu_lateral = document.getElementById("menu-lateral");
const header = document.getElementById("header");
const links = document.querySelectorAll("a");

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

function colorHeader() {
    if (window.scrollY > 250) {
        header.style.backgroundColor =
            "#262"; /* Vuelve a azul si estás arriba de los 100 píxeles */
    } else {
        header.style.backgroundColor =
            "#0608"; /* Cambia a rojo después de desplazar 100 píxeles */
    }
}
