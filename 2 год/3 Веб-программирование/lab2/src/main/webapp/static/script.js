(function(){
    const C = document.getElementById('plot');
    if(!C) return;
    const ctx = C.getContext('2d');
    const PAD = 24, RMAX = 5;
    
    function unit(){ return (Math.min(C.width, C.height) - PAD*2) / (RMAX*2); }
    function toPx(x,y){ const s=unit(), cx=C.width/2, cy=C.height/2; return {px: cx + x*s, py: cy - y*s}; }
    function toCoord(px,py){ const s=unit(), cx=C.width/2, cy=C.height/2; return {x:(px-cx)/s, y:-(py-cy)/s}; }
    function clear(){ ctx.clearRect(0,0,C.width,C.height); }
    function cssVar(name){ return getComputedStyle(document.documentElement).getPropertyValue(name).trim(); }

    // Оси координат
    function axes(r){
        const cx=C.width/2, cy=C.height/2;
        ctx.save();
        ctx.strokeStyle = cssVar('--muted');
        ctx.fillStyle   = cssVar('--muted');
        ctx.lineWidth=1;

        // Оси
        ctx.beginPath(); ctx.moveTo(PAD/2,cy); ctx.lineTo(C.width-PAD/2,cy); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(cx,PAD/2); ctx.lineTo(cx,C.height-PAD/2); ctx.stroke();

        // Стрелки
        ctx.beginPath(); ctx.moveTo(C.width-PAD/2,cy);
        ctx.lineTo(C.width-PAD/2-8,cy-4); ctx.lineTo(C.width-PAD/2-8,cy+4);
        ctx.closePath(); ctx.fill();

        ctx.beginPath(); ctx.moveTo(cx,PAD/2);
        ctx.lineTo(cx-4,PAD/2+8); ctx.lineTo(cx+4,PAD/2+8);
        ctx.closePath(); ctx.fill();

        // Засечки
        if(r){
            const ticks=[-r,-r/2,r/2,r];
            ctx.textAlign='center'; ctx.textBaseline='top';
            for(const t of ticks){ const {px}=toPx(t,0); ctx.beginPath(); ctx.moveTo(px,cy-4); ctx.lineTo(px,cy+4); ctx.stroke(); ctx.fillText(String(t),px,cy+6); }
            ctx.textAlign='right'; ctx.textBaseline='middle';
            for(const t of ticks){ const {py}=toPx(0,t); ctx.beginPath(); ctx.moveTo(cx-4,py); ctx.lineTo(cx+4,py); ctx.stroke(); ctx.fillText(String(t),cx-6,py); }
        }
        ctx.restore();
    }

    // Область
    function area(r){
        if(!r) return;
        ctx.save();
        ctx.fillStyle   = cssVar('--shade');
        ctx.strokeStyle = cssVar('--shade-stroke');
        ctx.lineWidth = 1;

        // q2
        (function(){
            const O = toPx(0,0), A = toPx(-r/2, 0), B = toPx(0, r/2);
            ctx.beginPath();
            ctx.moveTo(O.px, O.py);
            ctx.lineTo(A.px, A.py);
            ctx.lineTo(B.px, B.py);
            ctx.closePath(); ctx.fill(); ctx.stroke();
        })();

        // q3
        (function () {
            const c = toPx(0, 0);
            const R = unit() * r;
            ctx.beginPath();
            ctx.moveTo(c.px, c.py);
            ctx.arc(c.px, c.py, R, Math.PI/2, Math.PI, false);
            ctx.closePath();
            ctx.fill();
            ctx.stroke();
        })();

        // q4
        (function(){
            const a = toPx(0, -r), b = toPx(r/2, 0);
            ctx.beginPath();
            ctx.rect(a.px, a.py, b.px - a.px, b.py - a.py);
            ctx.fill(); ctx.stroke();
        })();
        ctx.restore();
    }

    // Масштабирование точек
    window.scalePoints = function(list, targetR){
        if (!targetR) return [];
        return (list || []).map(function(p){
            var r0 = Number(p.r) || targetR;
            var s  = r0 ? (targetR / r0) : 1;
            return { x: Number(p.x) * s, y: Number(p.y) * s, hit: !!p.hit };
        });
    };

    // Точки
    function drawPoints(list){
        if(!list) return;
        for(const p of list){
            const {px,py}=toPx(Number(p.x),Number(p.y));
            ctx.save();
            ctx.fillStyle = p.hit ? cssVar('--good') : cssVar('--bad');
            ctx.strokeStyle = cssVar('--fg');
            ctx.beginPath(); ctx.arc(px,py,4,0,Math.PI*2); ctx.fill(); ctx.stroke();
            ctx.restore();
        }
    }

    // Рендер
    window.renderScene = function(r, list){
        clear(); axes(r); area(r); drawPoints(list||[]);
        window.__lastRender = { r, points: (list||[]) };
    };

    // Клик по canvas
    C.addEventListener('click', function(e){
        const err = document.getElementById('err');
        const rRadio = document.querySelector('input[name="r"]:checked');

        if (!rRadio){
            if (err) err.textContent = 'Выберите R';   // inline как у формы
            return;
        } else {
            if (err) err.textContent = '';
        }

        const rect = C.getBoundingClientRect();
        const p = toCoord(e.clientX - rect.left, e.clientY - rect.top);

        // Берём корректный URL из формы
        const action = document.getElementById('hit-form').action;

        // Отправляем отдельной временной формой, чтобы не триггерить onsubmit-валидацию
        const f = document.createElement('form');
        f.method = 'post';
        f.action = action;

        const add = (n,v)=>{ const i=document.createElement('input'); i.type='hidden'; i.name=n; i.value=v; f.appendChild(i); };

        // Отправляем «как есть» (можно слегка ограничить длину записи)
        add('x', Number(p.x));
        add('y', Number(p.y));
        add('r', rRadio.value);

        document.body.appendChild(f);
        f.submit();
    });


    // Просмотр точки из истории
    document.addEventListener('click', function(e){
        const btn = e.target.closest('.btn-plot');
        if (!btn) return;

        const x = Number(btn.dataset.x);
        const y = Number(btn.dataset.y);
        const r = Number(btn.dataset.r);
        const hit = btn.dataset.hit === 'true';

        const rRadio = document.querySelector('input[name="r"][value="' + r + '"]');
        if (rRadio) rRadio.checked = true;

        document.querySelectorAll('#results tbody tr').forEach(tr => tr.classList.remove('active-row'));
        const tr = btn.closest('tr'); if (tr) tr.classList.add('active-row');

        renderScene(r, [{ x, y, hit }]);
    });

    // Просмотр всех точек
    document.addEventListener('click', function(e){
        const allBtn = e.target.closest('.btn-plot-all');
        if (!allBtn) return;

        let R = (typeof window.LAST_R === 'number') ? window.LAST_R : null;
        if (R == null) {
            const sel = document.querySelector('input[name="r"]:checked');
            if (!sel) { alert('Нет последнего R. Выберите R.'); return; }
            R = Number(sel.value);
            window.LAST_R = R;
        }

        const rRadio = document.querySelector('input[name="r"][value="' + R + '"]');
        if (rRadio) rRadio.checked = true;

        document.querySelectorAll('#results tbody tr').forEach(tr => tr.classList.remove('active-row'));

        const list = window.scalePoints(window.HISTORY_RAW || [], R);
        renderScene(R, list);
    });
})();