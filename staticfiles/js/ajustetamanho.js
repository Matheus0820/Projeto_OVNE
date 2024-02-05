window.addEventListener('DOMContentLoaded', (event) => {
    adjustBodyHeight();
});

window.addEventListener('resize', () => {
    adjustBodyHeight();
});

function adjustBodyHeight() {
    document.body.style.height = window.innerHeight + 'px';
}

