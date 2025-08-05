# CampusMate – Agent Roadmap

## 1. Bootstrap [DONE]
- Create project root “campusmate”. [DONE]
- Init git repo, add MIT LICENSE, .gitignore (Python, Node, macOS). [DONE]
- Scaffold docs/vision.md with the product description in <120 words. [DONE]
- Write README with setup commands: `make dev`, `make test`, `make lint`. [DONE]
- Add GitHub Actions workflow: run Ruff + Pytest + React tests on push. [DONE]

## 2. Skeleton App [DONE]
- `gem scaffold` FastAPI app with `/healthz` returning 200. [DONE]
- `gem scaffold` React app (Vite + Tailwind) with landing page. [DONE]
- Add Dockerfile.dev for backend, Dockerfile.dev for frontend, docker-compose.yml wiring Postgres + pgadmin. [DONE]
- Ensure `make dev` spins everything up. [DONE]

## 3. Domain Models [DONE]
- Define SQLAlchemy models: User, Class, Enrollment, StudyGroup, Membership. [DONE]
- Create Alembic migration and seed script (`python scripts/seed.py`). [DONE]
- Expose CRUD endpoints for User and StudyGroup. [DONE]

## 4. Matching Engine [DONE]
- Implement `/match` POST that accepts user_id and returns ranked list of study-group IDs. [DONE]
- Use cosine similarity of vectorized study habits + schedule overlap score. [DONE]
- Cache results in Redis with 10 min TTL. [DONE]

## 5. In-Person Features [DONE]
- Add `POST /groups/{id}/schedule` to propose meeting time. [DONE]
- Integrate Google Maps embed + ICS generator. [DONE]
- Hook up SendGrid or Twilio for reminders. [DONE]

## 6. Polish & Deploy [DONE]
- Add ESLint + Prettier, enable Ruff autofix. [DONE]
- Bundle Sentry SDK, healthcheck endpoint. [DONE]
- Provision Fly.io app via Terraform. [DONE]
- Document `QUICK_START.md`. [DONE]

## 7. Feedback Loop [DONE]
- Instrument basic events (signup, match_click, meetup_confirm). [DONE]
- Stream to PostHog cloud instance. [DONE]
- Nightly cron exports anonymized CSV to `/data/exports`. [DONE]