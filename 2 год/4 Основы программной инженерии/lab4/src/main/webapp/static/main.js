function selectX(value, checkbox) {
    const container = checkbox.closest('.x-options');

    if (container) {
        const boxes = container.querySelectorAll('input[type="checkbox"]');
        boxes.forEach(function (b) {
            if (b !== checkbox) { b.checked = false; }
        });
    }
    const hidden = document.getElementById('hit-form:xHidden');
    if (hidden) { hidden.value = String(value); }
}

// Изменение R
function onRSliderChange(raw) {
    const hidden = document.getElementById('hit-form:rHidden');
    const label  = document.getElementById('rValue');
    const normalized = String(raw).replace(',', '.');
    const withComma  = normalized.replace('.', ',');
    if (hidden) {
        hidden.value = withComma;
    }
    if (label) {
        label.textContent = 'R = ' + withComma;
    }
    if (window.updatePlotFromDom) {
        updatePlotFromDom(true);
    }
}

function afterAjaxUpdate(data) {
    if (data && data.status === 'success' && window.updatePlotFromDom) {
        updatePlotFromDom();
    }
}

<!-- График -->
(function () {
    const canvas = document.getElementById('plot');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    const cx = width / 2;
    const cy = height / 2;
    const scale = 40;

    function getColors() {
        const cs = getComputedStyle(document.documentElement);
        const bg = cs.getPropertyValue('--bg') || '#ffffff';
        const fg = cs.getPropertyValue('--fg') || '#000000';
        return {bg: bg.trim(), fg: fg.trim()};
    }

        function toCanvas(x, y) {
        return {
            x: cx + x * scale,
            y: cy - y * scale
        };
    }

    function readPointsFromTable() {
        const table = document.getElementById('results');
        const pts = [];
        if (!table || !table.tBodies.length) return pts;

        const body = table.tBodies[0];
        const rows = body.rows;

        for (let i = 0; i < rows.length; i++) {
            const cells = rows[i].cells;
            if (cells.length < 5) continue;

            const x = parseFloat(cells[1].innerText.replace(',', '.'));
            const y = parseFloat(cells[2].innerText.replace(',', '.'));
            const r = parseFloat(cells[3].innerText.replace(',', '.'));
            const hitText = cells[4].innerText.trim();
            const hit = hitText.startsWith('Да');
            const active = rows[i].classList.contains('active-row');

            if (!isNaN(x) && !isNaN(y) && !isNaN(r)) {
                pts.push({x, y, r, hit, active});
            }
        }
        return pts;
    }

    function formatTickValue(v) {
        let val = Math.round(v * 100) / 100;
        let s = String(val);
        if (s.indexOf('.') >= 0) {
            s = s.replace('.', ',');
        }
        return s;
    }

    // Рисования графика
    function drawScene(r, points) {
        const colors = getColors();

        ctx.clearRect(0, 0, width, height);
        ctx.fillStyle = colors.bg;
        ctx.fillRect(0, 0, width, height);

        ctx.save();
        ctx.strokeStyle = colors.fg;
        ctx.lineWidth = 1.5;

        // Оси
        // X
        ctx.beginPath();
        ctx.moveTo(0, cy);
        ctx.lineTo(width, cy);
        // Y
        ctx.moveTo(cx, 0);
        ctx.lineTo(cx, height);
        ctx.stroke();

        // Стрелки, Засечки, Подписи
        const arrow = 8;

        ctx.beginPath();
        ctx.moveTo(width - arrow, cy - arrow / 2);
        ctx.lineTo(width, cy);
        ctx.lineTo(width - arrow, cy + arrow / 2);
        ctx.stroke();

        ctx.beginPath();
        ctx.moveTo(cx - arrow / 2, arrow);
        ctx.lineTo(cx, 0);
        ctx.lineTo(cx + arrow / 2, arrow);
        ctx.stroke();

        const R = (!isNaN(r) && r > 0) ? r : 3;
        const ticks = [
            { val: -R,  label: formatTickValue(-R) },
            { val: -R/2,label: formatTickValue(-R/2) },
            { val: R/2, label: formatTickValue( R/2) },
            { val: R,   label: formatTickValue( R) }
        ];

        ctx.font = '12px system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif';
        ctx.fillStyle = colors.fg;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'top';
        ticks.forEach(function (t) {
            const p = toCanvas(t.val, 0);
            ctx.beginPath();
            ctx.moveTo(p.x, cy - 5);
            ctx.lineTo(p.x, cy + 5);
            ctx.stroke();
            ctx.fillText(t.label, p.x, cy + 8);
        });

        ctx.textAlign = 'right';
        ctx.textBaseline = 'middle';
        ticks.forEach(function (t) {
            const p = toCanvas(0, t.val);
            ctx.beginPath();
            ctx.moveTo(cx - 5, p.y);
            ctx.lineTo(cx + 5, p.y);
            ctx.stroke();
            ctx.fillText(t.label, cx - 8, p.y);
        });

        ctx.textAlign = 'right';
        ctx.textBaseline = 'bottom';
        ctx.fillText('X', width - 4, cy - 8);

        ctx.textAlign = 'left';
        ctx.textBaseline = 'top';
        ctx.fillText('Y', cx + 8, 4);

        // Область попадания
        ctx.fillStyle = 'rgba(80, 160, 255, 0.35)';
        const halfR = R / 2;
        let p;

        // Q1
        ctx.beginPath();
        p = toCanvas(0, 0);
        ctx.moveTo(p.x, p.y);
        const stepsCircle = 60;
        for (let i = 0; i <= stepsCircle; i++) {
            const angle = (Math.PI / 2) * (i / stepsCircle);
            const xx = halfR * Math.cos(angle);
            const yy = halfR * Math.sin(angle);
            const c = toCanvas(xx, yy);
            ctx.lineTo(c.x, c.y);
        }
        ctx.closePath();
        ctx.fill();

        // Q2
        ctx.beginPath();
        p = toCanvas(-halfR, 0);
        ctx.moveTo(p.x, p.y);
        p = toCanvas(0, 0);
        ctx.lineTo(p.x, p.y);
        p = toCanvas(0, R);
        ctx.lineTo(p.x, p.y);
        p = toCanvas(-halfR, R);
        ctx.lineTo(p.x, p.y);
        ctx.closePath();
        ctx.fill();

        // Q3
        ctx.beginPath();
        p = toCanvas(0, 0);
        ctx.moveTo(p.x, p.y);
        p = toCanvas(-halfR, 0);
        ctx.lineTo(p.x, p.y);
        p = toCanvas(0, -halfR);
        ctx.lineTo(p.x, p.y);
        ctx.closePath();
        ctx.fill();
        ctx.restore();

        // Точки
        points.forEach(function (pt) {
            const Rcur = R;
            const pointR = (!isNaN(pt.r) && pt.r > 0) ? pt.r : Rcur;
            const k = Rcur / pointR;
            const drawX = pt.x * k;
            const drawY = pt.y * k;
            const c = toCanvas(drawX, drawY);
            ctx.beginPath();
            const radiusPt = pt.active ? 6 : 4;
            ctx.arc(c.x, c.y, radiusPt, 0, 2 * Math.PI);
            ctx.fillStyle = pt.hit ? '#2ecc71' : '#e74c3c';
            ctx.fill();
            ctx.strokeStyle = colors.fg;
            ctx.lineWidth = pt.active ? 1.5 : 1;
            ctx.stroke();
        });
    }

    // Текущее R
    function getCurrentR() {
        let raw = null;
        const hidden = document.getElementById('hit-form:rHidden');
        if (hidden && hidden.value) {
            raw = hidden.value;
        }
        if (!raw) {
            const slider = document.getElementById('rSlider');
            if (slider && slider.value) {
                raw = slider.value;
            }
        }
        if (!raw) return 0;
        const rv = parseFloat(String(raw).replace(',', '.'));
        return isNaN(rv) ? 3 : rv;
    }

    // Все точки
    window.updatePlotFromDom = function (fromSlider) {
        const table = document.getElementById('results');
        if (!fromSlider && table && table.tBodies.length > 0) {
            const body = table.tBodies[0];
            const rows = body.rows;
            if (rows.length > 0) {
                let hasActive = false;
                for (let i = 0; i < rows.length; i++) {
                    if (rows[i].classList.contains('active-row')) {
                        hasActive = true;
                        break;
                    }
                }
                if (!hasActive) {
                    for (let i = 0; i < rows.length; i++) {
                        rows[i].classList.remove('active-row');
                    }
                    rows[0].classList.add('active-row');
                }
            }
        }
        const pts = readPointsFromTable();
        const r = getCurrentR();
        drawScene(r, pts);
    };

    // Одна точка
    window.__drawHitScene = function (r, points) {
        drawScene(r, points || []);
    };
    window.addEventListener('load', function () {
        const hiddenR = document.getElementById('hit-form:rHidden');
        const sliderR = document.getElementById('rSlider');
        const labelR  = document.getElementById('rValue');
        let start = 2;
        if (hiddenR && hiddenR.value) {
            const v = parseFloat(hiddenR.value.replace(',', '.'));
            if (!isNaN(v)) start = v;
        }
        if (sliderR) sliderR.value = start;
        if (labelR)  labelR.textContent = 'R = ' + String(start).replace('.', ',');
        updatePlotFromDom();
    });

    // Клик по графику
    canvas.addEventListener('click', function (evt) {
        const rect = canvas.getBoundingClientRect();
        const px = evt.clientX - rect.left;
        const py = evt.clientY - rect.top;
        const xVal = (px - cx) / scale;
        const yVal = (cy - py) / scale;
        const rx = Math.round(xVal * 1000) / 1000;
        const ry = Math.round(yVal * 1000) / 1000;
        const xHidden = document.getElementById('hit-form:xHidden');
        const yInput = document.getElementById('hit-form:y');
        const fromCanvas = document.getElementById('hit-form:fromCanvas');

        if (xHidden) xHidden.value = String(rx);
        if (yInput) yInput.value = String(ry);
        if (fromCanvas) fromCanvas.value = 'true';

        const xContainer = document.querySelector('.x-options');
        if (xContainer) {
            const boxes = xContainer.querySelectorAll('input[type="checkbox"]');
            boxes.forEach(function (b) { b.checked = false; });
        }

        const btn = document.getElementById('hit-form:checkBtn');
        if (btn) btn.click();
    });
})();

<!-- Показ точек из истории-->
function showAllPoints() {
    const table = document.getElementById('results');
    if (table && table.tBodies.length > 0) {
        const tbody = table.tBodies[0];
        const rows = tbody.rows;
        for (let i = 0; i < rows.length; i++) {
            rows[i].classList.remove('active-row');
        }
        if (rows.length > 0) {
            rows[0].classList.add('active-row');
        }
    }
    if (window.updatePlotFromDom) {
        updatePlotFromDom();
    }
}

function showPointFromRow(button) {
    const row = button.closest('tr');
    if (!row) return;
    const cells = row.cells;
    if (cells.length < 5) return;
    const x = parseFloat(cells[1].innerText.replace(',', '.'));
    const y = parseFloat(cells[2].innerText.replace(',', '.'));
    const r = parseFloat(cells[3].innerText.replace(',', '.'));
    const hitText = cells[4].innerText.trim();
    const hit = hitText.startsWith('Да');

    if (isNaN(x) || isNaN(y) || isNaN(r)) return;
    const tbody = row.parentNode;
    if (tbody) {
        for (let i = 0; i < tbody.rows.length; i++) {
            tbody.rows[i].classList.remove('active-row');
        }
    }
    row.classList.add('active-row');
    if (window.__drawHitScene) {
        window.__drawHitScene(r, [{
            x: x,
            y: y,
            r: r,
            hit: hit,
            active: true
        }]);
    }
}