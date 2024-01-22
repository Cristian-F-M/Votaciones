
progress()



window.addEventListener('scroll', () => {
    progress()
});


function progress() {
    let progress = document.getElementById('progress');
    let windowHeight = window.innerHeight;
    let documentHeight = document.documentElement.scrollHeight;
    let scrollTop = window.scrollY;

    let indicatorHeight = porcentage(scrollTop, documentHeight, windowHeight)
    indicatorHeight < 50 ? progress.classList.add('less') : progress.classList.remove('less')
    indicatorHeight = ((windowHeight - documentHeight) === 0) ? 100 : indicatorHeight

    progress.style.setProperty('--i', indicatorHeight);

    animarIcono(windowHeight, documentHeight, scrollTop)

}


function porcentage(scrollTop, documentHeight, windowHeight) {
    let scrollPercentage = (scrollTop / (documentHeight - windowHeight)) * 100;
    let indicatorHeight = Math.min(scrollPercentage, 100);
    return indicatorHeight
}



function animarIcono(windowHeight, documentHeight, scrollTop) {
    let indicatorHeight = porcentage(scrollTop, documentHeight, windowHeight)
    let a_arrowUp = document.getElementById('a_arrow-up');

    if (indicatorHeight === 0) {
        a_arrowUp.removeAttribute('up', '');
        a_arrowUp.setAttribute('down', '');
        a_arrowUp.href = "#Footer"
    } else {
        a_arrowUp.removeAttribute('down', '');
        a_arrowUp.setAttribute('up', '');
        a_arrowUp.href = "#Inicio"
    }
}
