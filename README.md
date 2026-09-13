# Cross-Platform Multi-Device Monitoring Platform

A centralized monitoring system where a user registers multiple computers (any OS) under one account and views their live status — CPU, RAM, disk, and online/offline state — from a single web dashboard.

Built as an 8-day MVP project for learning Django REST Framework, React, and distributed-system fundamentals (device authentication, heartbeats, and telemetry pipelines).

## Architecture

```
Monitoring Agent (Python)  --HTTPS-->  Django REST API  <-->  React Dashboard
     (runs on each device)              |
                                         v
                                    PostgreSQL
```

- **Monitoring agent** — a lightweight Python script that runs on each machine. Collects CPU/RAM/disk stats via `psutil` and reports them to the backend over authenticated HTTPS. Never receives inbound connections — all communication is outbound, so the server can never execute anything on the monitored machine.
- **Django REST API** — the central hub. Handles user auth (JWT), device registration, telemetry ingestion, and serves data to the frontend.
- **PostgreSQL** — stores users, devices, and telemetry readings.
- **React dashboard** — lets a logged-in user see all their registered devices, online/offline status, and live resource usage, with polling-based auto-refresh.

## Data model

**Device**
| Field | Notes |
|---|---|
| owner | FK to User |
| name | e.g. "Arch Linux Laptop" |
| os_type | e.g. "linux" |
| token | auto-generated, 64-char hex, used for agent authentication |
| last_seen | updated on every heartbeat/telemetry POST |

`is_online` is **not** a stored field — it's a computed property: `(now - last_seen) < 30 seconds`. This keeps it from ever drifting out of sync with reality.

**Telemetry**
| Field | Notes |
|---|---|
| device | FK to Device |
| timestamp | auto-set |
| cpu_percent, memory_percent, disk_percent | |

## Authentication — two separate systems

| Who | Method | Header |
|---|---|---|
| React user | JWT (`djangorestframework-simplejwt`) | `Authorization: Bearer <access_token>` |
| Monitoring agent | Custom device-token auth (`DeviceTokenAuthentication`) | `Authorization: Token <device_token>` |

Users log in with a username/password and get a short-lived access token + long-lived refresh token. An axios response interceptor on the frontend silently refreshes an expired access token and retries the failed request — the user never sees a forced logout mid-session.

Agents never see a username/password — only a random token generated at device-registration time, scoped to exactly one device.

## API endpoints

| Method | Endpoint | Caller | Purpose |
|---|---|---|---|
| POST | `/api/auth/login/` | React | returns JWT access + refresh tokens |
| POST | `/api/auth/refresh/` | React | exchanges refresh token for new access token |
| GET / POST | `/api/devices/` | React | list / register devices (scoped to logged-in user) |
| POST | `/api/telemetry/` | Agent | submit one telemetry reading (device-token auth) |
| POST | `/api/heartbeat/` | Agent | update `last_seen` only |
| GET | `/api/devices/<id>/telemetry/` | React | latest readings for one device (owner-checked) |

## Tech stack

- **Agent**: Python, `psutil`, `requests`
- **Backend**: Django, Django REST Framework, `djangorestframework-simplejwt`, `django-cors-headers`, PostgreSQL
- **Frontend**: React (Vite), `axios`, `react-router-dom`

## Setup

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install django djangorestframework psycopg2-binary djangorestframework-simplejwt python-decouple django-cors-headers

# create .env with DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, SECRET_KEY
# create the PostgreSQL database + user matching .env

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173/login`.

### Agent

```bash
cd monitoring-agent
python -m venv venv
source venv/bin/activate
pip install psutil requests

python agent.py --server http://localhost:8000 --token <device-token-from-dashboard>
```

Register a device from the dashboard first to get its token.

## MVP scope (done)

- [x] User authentication (JWT login + silent refresh)
- [x] Device registration with unique per-device tokens
- [x] Linux monitoring agent (CPU/RAM/disk via `psutil`)
- [x] Authenticated telemetry submission (device-token auth)
- [x] PostgreSQL storage
- [x] React dashboard with polling-based live updates
- [x] Heartbeat-based online/offline detection
- [x] Multi-device support per account, with per-user data isolation

## Post-MVP roadmap

- [ ] Historical usage graphs (last hour / day / week)
- [ ] Network stats and process-level monitoring
- [ ] Windows agent (same `psutil`-based approach, different packaging)
- [ ] WebSocket-based real-time updates (replace polling)
- [ ] Alerting (CPU/memory/disk thresholds, device-offline alerts) with email/Discord/Telegram notifications
- [ ] Local telemetry buffering on the agent during server downtime, with retry + exponential backoff
- [ ] Agent auto-start (systemd service on Linux, Windows service on Windows)
- [ ] Production deployment: proper HTTPS, environment-based settings, rate limiting

## Key lessons from building this

- **Ownership filtering** (`get_queryset` filtered by `owner=request.user`) is what actually enforces multi-tenant data isolation — without it, `ModelViewSet` defaults to returning everyone's data.
- **Compute derived state, don't store it** — `is_online` as a property (not a DB column) can never drift out of sync with `last_seen`.
- **Two authentication systems for two kinds of caller** — a human user (JWT) and a machine agent (device token) have different security needs and shouldn't share one mechanism.
- **Silent token refresh via axios interceptors** keeps short-lived access tokens secure without disrupting the user session.
- **`include()` URL prefixes need trailing slashes** in Django, or the stripped-prefix math breaks matching in confusing ways.
