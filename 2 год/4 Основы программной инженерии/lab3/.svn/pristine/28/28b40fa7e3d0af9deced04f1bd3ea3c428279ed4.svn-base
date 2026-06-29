(function () {
    const root = document.documentElement;
    const btn = document.getElementById('theme-toggle');
    if (!btn) return;

    const KEY = 'theme';

    function apply(theme) {
        root.setAttribute('data-theme', theme);
        btn.textContent = (theme === 'dark') ? '☀️ Тема' : '🌙 Тема';

        if (window.updatePlotFromDom) {
            window.updatePlotFromDom();
        }
        if (window.__redrawAnalogClock) {
            window.__redrawAnalogClock();
        }
    }

    const saved = localStorage.getItem(KEY);
    const prefersDark =
        window.matchMedia &&
        window.matchMedia('(prefers-color-scheme: dark)').matches;

    apply(saved ? saved : (prefersDark ? 'dark' : 'light'));

    btn.addEventListener('click', function () {
        const next = (root.getAttribute('data-theme') === 'dark') ? 'light' : 'dark';
        localStorage.setItem(KEY, next);
        apply(next);
    });
})();
