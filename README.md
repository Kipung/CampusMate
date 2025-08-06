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
*   **Backend Functionality (Automated API Tests):**
    *   All API endpoints (Health Checks, User Management, Study Group Management, Matching Engine, In-Person Features) have been successfully tested via automated scripts.
*   **Cron Job (Data Export):**
    *   Automated data export to `data/exports/export.csv` is confirmed working.
*   **Automated Checks:**
    *   `make test` (backend and frontend unit tests) are passing.
    *   `make lint` (backend and frontend code linting) are passing.

### Still to Test:

*   **Manual UI/UX Verification:**
    *   Thorough manual testing of the frontend user interface and user experience.
    *   Verification of all interactive elements and workflows.
*   **External Service Integration (Manual Verification):**
    *   If actual SendGrid/Twilio credentials are provided, verify email/SMS reminders are sent.
*   **Deployment Verification:**
    *   Verify successful deployment to Fly.io once configured with actual credentials.