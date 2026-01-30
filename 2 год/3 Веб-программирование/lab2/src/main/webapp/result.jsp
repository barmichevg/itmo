<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Результат проверки</title>
    <link rel="stylesheet" href="<%=request.getContextPath()%>/static/style.css">
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
</head>
<body>
<div class="header-wrap">
    <h1>Результат проверки</h1>
    <small>Веб-программирование — Лабораторная работа №2</small>
</div>

<div class="card" style="max-width:720px; margin: 0 auto 16px;">
    <table class="form" style="width:100%">
        <tr><td style="width:140px;">X:</td><td><%= request.getAttribute("x") %></td></tr>
        <tr><td>Y:</td><td><%= request.getAttribute("y") %></td></tr>
        <tr><td>R:</td><td><%= request.getAttribute("r") %></td></tr>
        <tr><td>Попадание:</td>
            <td>
                <%
                    Boolean hit = (Boolean) request.getAttribute("hit");
                    out.print(hit != null && hit ? "<span class='good'>Да</span>" : "<span class='bad'>Нет</span>");
                %>
            </td>
        </tr>
        <tr><td>Время запроса:</td><td><%= request.getAttribute("at") %></td></tr>
        <tr><td>Время скрипта, μs:</td><td><%= request.getAttribute("scriptMicros") %></td></tr>
    </table>
</div>

<div id="canvas-wrap" style="text-align:center; margin-bottom:16px;">
    <canvas id="plot" width="720" height="420"></canvas>
</div>

<div style="text-align:center; margin-bottom:24px;">
    <a class="btn" href="<%=response.encodeURL(request.getContextPath()+"/controller")%>">Новый запрос</a>
</div>

<!-- скрипты графика -->
<script src="<%=request.getContextPath()%>/static/script.js?v=8"></script>

<!-- отрисовка точки -->
<script>
    (function(){
        var x = Number("<%= request.getAttribute("x") %>");
        var y = Number("<%= request.getAttribute("y") %>");
        var r = Number("<%= request.getAttribute("r") %>");
        var hit = <%
      Boolean h = (Boolean) request.getAttribute("hit");
      out.print(h != null && h ? "true" : "false");
  %>;

        if (typeof renderScene === 'function') {
            renderScene(r, [{ x: x, y: y, hit: hit }]);
        }
        window.__lastRender = { r: r, points: [{ x: x, y: y, hit: hit }] };
    })();
</script>

<!-- тема -->
<script>
    (function(){
        const root = document.documentElement;
        const KEY  = 'theme';
        const mq   = window.matchMedia('(prefers-color-scheme: dark)');

        function apply(theme){
            root.setAttribute('data-theme', theme);
            if (typeof renderScene === 'function' && window.__lastRender){
                renderScene(window.__lastRender.r, window.__lastRender.points);
            }
        }

        const saved = localStorage.getItem(KEY);
        if (saved === 'dark' || saved === 'light') {
            apply(saved);
        } else {
            apply(mq.matches ? 'dark' : 'light');
            mq.addEventListener('change', (e)=> apply(e.matches ? 'dark' : 'light'));
        }
    })();
</script>
</body>
</html>
