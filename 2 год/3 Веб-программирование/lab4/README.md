# ЛР4 (Spring Boot + Vue + REST)

## Быстрый старт

### 1) База (PostgreSQL)
В корне проекта:
```bash
docker compose up -d
```

### 2) Backend
```bash
./gradlew :backend:bootRun
```
Backend стартует на http://localhost:8080

Тестовый пользователь создаётся при старте:
- login: admin
- password: admin

### 3) Frontend (Vue)
В папке `frontend/`:
```bash
npm i
npm run dev
```
Frontend: http://localhost:5173

В dev режиме запросы `/api/**` проксируются на backend, cookie-сессия работает через `credentials: 'include'`.
