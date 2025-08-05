# CampusMate

## Setup

```bash
make dev
make test
make lint
```

## Project Status

All major features outlined in the roadmap have been implemented:

*   **Bootstrap:** Project setup, Git, documentation, and CI workflow are complete.
*   **Skeleton App:** Basic FastAPI backend and React frontend are scaffolded and integrated with Docker Compose.
*   **Domain Models:** SQLAlchemy models are defined, and Alembic migrations and seeding are set up.
*   **Matching Engine:** User-to-study group matching based on study habits and schedule overlap is implemented.
*   **In-Person Features:** Functionality for scheduling, location, map integration, ICS generation, and reminder placeholders are in place.
*   **Polish & Deploy:** Sentry and PostHog integration are added, and `QUICK_START.md` is documented.
*   **Feedback Loop:** Event instrumentation and nightly data export mechanisms are set up.

## Testing Status

Here's a record of what has been tested and confirmed working, and what still needs verification:

### Confirmed Working:

*   **Application Access:**
    *   Frontend (`http://localhost:3000`) loads and displays content.
    *   Backend API Docs (Swagger UI at `http://localhost:8001/docs`) are accessible.
    *   pgAdmin (`http://localhost:5050`) is accessible and successfully connected to the `campusmate` database.
*   **Backend Functionality (via Swagger UI):**
    *   `GET /healthz` endpoint returns `200 OK`.
    *   `GET /healthcheck` endpoint returns `200 OK`.
    *   `POST /users/` successfully creates a user, and the data can be verified in pgAdmin.

### Still to Test:

*   **Backend Functionality (via Swagger UI):**
    *   `GET /users/` (retrieve all users)
    *   `GET /users/{user_id}` (retrieve a specific user)
    *   `POST /study_groups/` (create a new study group)
    *   `GET /study_groups/` (retrieve all study groups)
    *   `GET /study_groups/{study_group_id}` (retrieve a specific study group)
    *   `POST /match` (get ranked study group recommendations)
    *   `POST /groups/{group_id}/schedule` (update study group meeting time)
    *   `POST /groups/{group_id}/location` (update study group location)
    *   `GET /groups/{group_id}/map` (get Google Maps embed URL)
    *   `GET /groups/{group_id}/ics` (get ICS file for meeting)
    *   `POST /groups/{group_id}/remind` (trigger email reminder)
*   **Cron Job (Data Export):**
    *   Manually trigger `docker-compose exec backend python scripts/export.py` and verify `data/exports/export.csv` content.
*   **Automated Checks:**
    *   Run `make test` (backend and frontend unit tests).
    *   Run `make lint` (backend and frontend code linting).