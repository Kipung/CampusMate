# CampusMate – Agent Roadmap

## 1. Bootstrap
- Create project root “campusmate”.
- Init git repo, add MIT LICENSE, .gitignore (Python, Node, macOS).
- Scaffold docs/vision.md with the product description in <120 words.
- Write README with setup commands: `make dev`, `make test`, `make lint`.
- Add GitHub Actions workflow: run Ruff + Pytest + React tests on push.

## 2. Skeleton App
- `gem scaffold` FastAPI app with `/healthz` returning 200.
- `gem scaffold` React app (Vite + Tailwind) with landing page.
- Add Dockerfile.dev for backend, Dockerfile.dev for frontend, docker-compose.yml wiring Postgres + pgadmin.
- Ensure `make dev` spins everything up.

## 3. Domain Models
- Define SQLAlchemy models: User, Class, Enrollment, StudyGroup, Membership.
- Create Alembic migration and seed script (`python scripts/seed.py`).
- Expose CRUD endpoints for User and StudyGroup.

## 4. Matching Engine
- Implement `/match` POST that accepts user_id and returns ranked list of study-group IDs.
- Use cosine similarity of vectorized study habits + schedule overlap score.
- Cache results in Redis with 10 min TTL.

## 5. In-Person Features
- Add `POST /groups/{id}/schedule` to propose meeting time.
- Integrate Google Maps embed + ICS generator.
- Hook up SendGrid or Twilio for reminders.

## 6. Polish & Deploy
- Add ESLint + Prettier, enable Ruff autofix.
- Bundle Sentry SDK, healthcheck endpoint.
- Provision Fly.io app via Terraform.
- Document `QUICK_START.md`.

## 7. Feedback Loop
- Instrument basic events (signup, match_click, meetup_confirm).
- Stream to PostHog cloud instance.
- Nightly cron exports anonymized CSV to `/data/exports`.
