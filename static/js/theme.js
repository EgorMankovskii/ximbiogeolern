(function () {
    const storageKey = 'pyteacher-theme';
    const button = document.querySelector('[data-theme-toggle]');
    const icon = document.querySelector('[data-theme-icon]');

    function applyTheme(theme) {
        document.body.dataset.theme = theme;
        if (icon) {
            icon.textContent = theme === 'dark' ? '☀' : '☾';
        }
    }

    const savedTheme = localStorage.getItem(storageKey);
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    applyTheme(savedTheme || (prefersDark ? 'dark' : 'light'));

    if (button) {
        button.addEventListener('click', function () {
            const nextTheme = document.body.dataset.theme === 'dark' ? 'light' : 'dark';
            localStorage.setItem(storageKey, nextTheme);
            applyTheme(nextTheme);
        });
    }
}());
