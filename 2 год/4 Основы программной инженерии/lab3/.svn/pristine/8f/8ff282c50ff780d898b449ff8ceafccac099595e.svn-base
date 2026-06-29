(function () {
    const canvas = document.getElementById('analog-clock');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const radius = canvas.width / 2;
    ctx.translate(radius, radius);
    const clockRadius = radius * 0.9;

    function getClockColors() {
        const cs = getComputedStyle(document.documentElement);
        const bg = cs.getPropertyValue('--panel') || cs.getPropertyValue('--bg') || '#ffffff';
        const fg = cs.getPropertyValue('--fg') || '#000000';
        const accent = cs.getPropertyValue('--bad') || '#e74c3c';
        return {
            bg: bg.trim(),
            fg: fg.trim(),
            accent: accent.trim()
        };
    }

    // отрисовка циферблата
    function drawFace() {
        const colors = getClockColors();

        ctx.clearRect(-radius, -radius, canvas.width, canvas.height);

        // циферблат
        ctx.beginPath();
        ctx.arc(0, 0, clockRadius, 0, 2 * Math.PI);
        ctx.fillStyle = colors.bg;
        ctx.fill();

        ctx.lineWidth = 4;
        ctx.strokeStyle = colors.fg;
        ctx.stroke();

        // деления 12
        ctx.save();
        ctx.lineWidth = 2;
        ctx.strokeStyle = colors.fg;
        for (let i = 0; i < 12; i++) {
            const angle = i * Math.PI / 6 - Math.PI / 2;
            ctx.beginPath();
            ctx.rotate(angle);
            ctx.moveTo(clockRadius * 0.8, 0);
            ctx.lineTo(clockRadius * 0.9, 0);
            ctx.stroke();
            ctx.rotate(-angle);
        }
        ctx.restore();
    }

    // отрисовка стрелок
    function drawHands(date) {
        const colors = getClockColors();
        ctx.lineCap = 'round';

        const seconds = date.getSeconds();
        const minutes = date.getMinutes();
        const hours = date.getHours() % 12;

        // часовая
        let angle = (hours + minutes / 60) * Math.PI / 6 - Math.PI / 2;
        ctx.beginPath();
        ctx.strokeStyle = colors.fg;
        ctx.lineWidth = 5;
        ctx.rotate(angle);
        ctx.moveTo(0, 0);
        ctx.lineTo(clockRadius * 0.5, 0);
        ctx.stroke();
        ctx.rotate(-angle);

        // минутная
        angle = (minutes + seconds / 60) * Math.PI / 30 - Math.PI / 2;
        ctx.beginPath();
        ctx.lineWidth = 3;
        ctx.strokeStyle = colors.fg;
        ctx.rotate(angle);
        ctx.moveTo(0, 0);
        ctx.lineTo(clockRadius * 0.75, 0);
        ctx.stroke();
        ctx.rotate(-angle);

        // секундная
        angle = seconds * Math.PI / 30 - Math.PI / 2;
        ctx.beginPath();
        ctx.lineWidth = 2;
        ctx.strokeStyle = colors.accent;
        ctx.rotate(angle);
        ctx.moveTo(0, 0);
        ctx.lineTo(clockRadius * 0.8, 0);
        ctx.stroke();
        ctx.rotate(-angle);

        // центр
        ctx.beginPath();
        ctx.fillStyle = colors.fg;
        ctx.arc(0, 0, 4, 0, 2 * Math.PI);
        ctx.fill();
    }

    function drawClock() {
        const now = new Date();
        drawFace();
        drawHands(now);
    }

    window.__redrawAnalogClock = drawClock;
    drawClock();
    setInterval(drawClock, 5000);
})();

(function () {
    function updateClock() {
        const el = document.getElementById('clock');
        if (!el) return;
        const now = new Date();
        el.textContent = now.toLocaleString('ru-RU', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
    }
    updateClock();
    setInterval(updateClock, 5000);
})();