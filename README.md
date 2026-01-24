# Legalmind AI

Skeleton project layout for a dual-team setup:

- Developer A: FastAPI backend and ML pipeline
- Developer B: Next.js frontend

## Structure

- client/: Next.js app (App Router), components, hooks, and libs
- server/: FastAPI app with API, core, models, and services
- ml_pipeline/: RAG engines, vector DB setup, prompt templates, and processors
- docker-compose.yml: Dev stack for frontend, backend, and Postgres

## Quickstart

1) Copy env vars into `.env` files for server and client as needed.
2) Run `docker-compose up --build` to start dev services.
3) Frontend: http://localhost:3000, Backend: http://localhost:8000/health, DB: Postgres on 5432.

## Next Steps

- Add Dockerfiles for frontend/backend if you prefer custom images.
- Implement auth, document upload endpoints, and chat routes under server/app/api/.
- Wire TanStack Query hooks to backend endpoints and build chat/PDF UI.
- Fill ml_pipeline modules with your RAG, embedding, and parsing logic.
