const menuButton = document.querySelector('[data-studio-menu]');

if (menuButton) {
    menuButton.addEventListener('click', () => {
        document.body.classList.toggle('studio-menu-open');
    });
}

document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
        document.body.classList.remove('studio-menu-open');
    }
});
