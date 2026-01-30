<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!doctype html>
<html lang="ru">

<head>
    <meta charset="UTF-8">
    <title>ЛР2 — Попадание точки</title>
    <link rel="stylesheet" href="<%=request.getContextPath()%>/static/style.css">
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
</head>

<body>
<button id="theme-toggle" class="theme-btn" type="button" aria-label="Переключить тему">🌙 Тема</button>
<div class="header-wrap">
    <h1>Бармичев Григорий Андреевич — P3210</h1>
    <small>Веб-программирование — Лабораторная работа #2 — Вариант 2152</small>
</div>

<!-- Форма ввода -->
<table class="layout">
    <tr>
        <td style="width:440px">
            <form id="hit-form" class="controls" action="<%=request.getContextPath()%>/controller" method="post" onsubmit="return validateAndSend(this)">
                <table class="form">
                    <tr><td>X:</td><td><input name="x" type="text" placeholder="-5 .. 5"/></td></tr>
                    <tr><td>Y:</td><td>
                        <%
                            int[] ys = {-4,-3,-2,-1,0,1,2,3,4};
                            for (int yy : ys) { %>
                        <label><input type="radio" name="y" value="<%=yy%>"><%=yy%></label>
                        <% } %>
                    </td></tr>
                    <tr><td>R:</td><td>
                        <%
                            int[] rs = {1,2,3,4,5};
                            for (int rr : rs) { %>
                        <label><input type="radio" name="r" value="<%=rr%>"><%=rr%></label>
                        <% } %>
                    </td></tr>
                    <tr><td><button class="btn" type="submit">Проверить</button></td><td>
                        <span id="err" class="error" style="margin-left:8px;"><%
                            String error = (String) request.getAttribute("error");
                            if (error != null && !error.isEmpty()) { out.print(error); }
                        %></span>
                    </td></tr>
                </table>
            </form>
            <form action="<%=request.getContextPath()%>/controller" method="post" style="margin-top:6px">
                <input type="hidden" name="clear" value="1">
                <button class="btn" type="submit">Очистить историю</button>
            </form>
            <%
                web.models.HitResult last = (web.models.HitResult) request.getAttribute("last");
                if (last != null) {
            %>
            <p class="last-check" style="margin-top:8px">
                Последняя проверка: (x=<%=last.x%>, y=<%=last.y%>, r=<%=last.r%>) →
                <strong class="<%= last.hit ? "good":"bad" %>"><%= last.hit ? "ПОПАДАНИЕ" : "МИМО" %></strong>
            </p>
            <%
                }
            %>
        </td>
        <td>
            <canvas id="plot" width="720" height="420"></canvas>
        </td>
    </tr>
</table>

<!-- История -->
<div class="history-box" style="margin-top:12px">
    <table id="results">
        <thead>
        <tr>
            <th class="col-actions" title="Показать все точки">
                <button type="button" class="btn btn-small btn-plot-all" aria-label="Показать все точки">▶</button>
            </th>
            <th class="col-x">X</th>
            <th>Y</th>
            <th>R</th>
            <th>Попадание</th>
            <th>Время</th>
            <th>Время скрипта, μs</th>
        </tr>
        </thead>
        <tbody>
        <%
            java.util.List rows = (java.util.List) request.getAttribute("history");
            if (rows != null) {
                for (int i = rows.size() - 1; i >= 0; i--) {
                    web.models.HitResult row = (web.models.HitResult) rows.get(i);
        %>
        <tr>
            <td>
                <button type="button"
                        class="btn btn-small btn-plot"
                        title="Показать на графике"
                        aria-label="Показать на графике"
                        data-x="<%=row.x%>" data-y="<%=row.y%>"
                        data-r="<%=row.r%>" data-hit="<%=row.hit%>">▶</button>
            </td>
            <td class="col-x" title="<%=row.x%>"><%=row.x%></td>
            <td><%=row.y%></td>
            <td><%=row.r%></td>
            <td><%=row.hit ? "Да" : "Нет"%></td>
            <td><%=row.at%></td>
            <td><%=row.scriptMicros%></td>
        </tr>
        <%
                }
            }
        %>
        </tbody>
    </table>
</div>

<!-- валидация формы -->
<script>
    function validateAndSend(form){
        const x = form.x.value.trim(), y = form.y.value, r = form.r.value;
        const err = document.getElementById('err'); err.textContent = '';
        if (x==='' || isNaN(x) || Number(x)<-5 || Number(x)>5){ err.textContent='X: число в диапазоне [-5;5]'; return false; }
        if (!y){ err.textContent='Выберите Y'; return false; }
        if (!r){ err.textContent='Выберите R'; return false; }
        return true;
    }
</script>

<!-- скрипты графика -->
<script src="<%=request.getContextPath()%>/static/script.js"></script>

<!-- инициализация графика и истории -->
<script>
    (function(){
        var HISTORY_RAW = (function(){
            var a = [];
            <%
              java.util.List histList = (java.util.List) request.getAttribute("history");
              if (histList != null) {
                for (int i = histList.size() - 1; i >= 0; i--) {
                  web.models.HitResult r = (web.models.HitResult) histList.get(i);
            %>
            a.push({ x:Number("<%=r.x%>"), y:Number("<%=r.y%>"),
                r:Number("<%=r.r%>"), hit:<%=r.hit%> });
            <%
                }
              }
            %>
            return a;
        })();

        var LAST = <%
        web.models.HitResult l = (web.models.HitResult) request.getAttribute("last");
        if (l != null) { out.print("{x:"+l.x+",y:"+l.y+",r:"+l.r+",hit:"+(l.hit?"true":"false")+"}"); }
        else { out.print("null"); }
        %>;

      window.HISTORY_RAW = HISTORY_RAW;
      window.LAST_R = LAST ? Number(LAST.r) : null;

      function currentR(){
          var sel = document.querySelector('input[name="r"]:checked');
          return sel ? Number(sel.value) : (window.LAST_R != null ? window.LAST_R : null);
      }

      (function init(){
          var R = currentR();
          if (R != null) renderScene(R, scalePoints(HISTORY_RAW, R));
          else renderScene(null, []);
      })();

      document.querySelectorAll('input[name="r"]').forEach(function(radio){
          radio.addEventListener('change', function(){
                var R = Number(this.value);
                renderScene(R, scalePoints(HISTORY_RAW, R));
            });
        });
    })();
</script>

<!-- переключатель темы -->
<script>
    (function(){
        const root = document.documentElement;
        const btn  = document.getElementById('theme-toggle');
        const KEY  = 'theme';
        function apply(theme){
            root.setAttribute('data-theme', theme);
            btn.textContent = (theme === 'dark') ? '☀️ Тема' : '🌙 Тема';
            if (window.__lastRender) renderScene(window.__lastRender.r, window.__lastRender.points);
        }
        const saved = localStorage.getItem(KEY);
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        apply(saved ? saved : (prefersDark ? 'dark' : 'light'));
        btn.addEventListener('click', () => {
            const next = (root.getAttribute('data-theme') === 'dark') ? 'light' : 'dark';
            localStorage.setItem(KEY, next); apply(next);
        });
    })();
</script>
</body>
</html>