# GEO AI Visibility System

An implementation of the revised GEO plan:
- Positioning: AI visibility operations (not ranking guarantee)
- Delivery: GEO Score + evidence chain
- Stack: FastAPI + PostgreSQL + Redis/Celery + Next.js + Docker Compose

## Repo Structure

```text
apps/api      FastAPI backend, orchestrator, scoring, compliance endpoints
apps/web      Next.js internal console
infra         Nginx and Postgres init
docs          SOP, disclaimer template, milestone guide
```

## Quick Start (Local)

1. Copy env file:

```bash
cp .env.example .env
```

2. Start all services:

```bash
docker compose up --build -d
```

3. Verify:

- API health: `http://localhost/healthz`
- Web console: `http://localhost`
- OpenAPI docs: `http://localhost:8000/docs`

## Key API Endpoints

- `POST /api/v1/auth/login`
- `POST /api/v1/clients`
- `POST /api/v1/diagnostics/jobs`
- `POST /api/v1/diagnostics/responses/import`
- `POST /api/v1/analysis/jobs`
- `POST /api/v1/analysis/recompute`
- `POST /api/v1/content/jobs`
- `POST /api/v1/ops/schedules`
- `POST /api/v1/reports/tracking`
- `POST /api/v1/reports/compliance-check`
- `GET /api/v1/reports/{client_id}`
- `GET /api/v1/tasks/{task_id}`

## Promise Boundary (Product Policy)

This system improves AI visibility metrics and execution quality.
It does not guarantee specific ranking or guaranteed recommendations.

