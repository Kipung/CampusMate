from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import redis
import json
import posthog
from datetime import datetime, timedelta

import crud
import models
import schemas
import matching
import integrations
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

# sentry_sdk.init(
#     dsn="YOUR_SENTRY_DSN",
#     traces_sample_rate=1.0,
# )

posthog.api_key = "YOUR_POSTHOG_API_KEY"
posthog.host = "YOUR_POSTHOG_HOST"

app = FastAPI()

redis_client = redis.Redis(host='redis', port=6379, db=0)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/study_groups/", response_model=schemas.StudyGroup)
def create_study_group(
    study_group: schemas.StudyGroupCreate, db: Session = Depends(get_db)
):
    return crud.create_study_group(db=db, study_group=study_group)


@app.get("/study_groups/", response_model=list[schemas.StudyGroup])
def read_study_groups(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    study_groups = crud.get_study_groups(db, skip=skip, limit=limit)
    return study_groups


@app.get("/study_groups/{study_group_id}", response_model=schemas.StudyGroup)
def read_study_group(study_group_id: int, db: Session = Depends(get_db)):
    db_study_group = crud.get_study_group(db, study_group_id=study_group_id)
    if db_study_group is None:
        raise HTTPException(status_code=404, detail="Study group not found")
    return db_study_group

@app.post("/match")
def match(user_id: int, db: Session = Depends(get_db)):
    cached_results = redis_client.get(f"user:{user_id}:matches")
    if cached_results:
        return json.loads(cached_results)

    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    study_groups = crud.get_study_groups(db)

    user_habits = user.study_habits
    group_habits = [group.study_habits for group in study_groups]
    user_schedule = user.schedule
    group_schedules = [group.schedule for group in study_groups]

    recommendations = matching.get_recommendations(user_habits, group_habits, user_schedule, group_schedules)

    ranked_groups = []
    for group_index, score in recommendations:
        ranked_groups.append({"study_group_id": study_groups[group_index].id, "score": score})

    redis_client.set(f"user:{user_id}:matches", json.dumps(ranked_groups), ex=600)

    

    return ranked_groups

@app.post("/groups/{group_id}/schedule", response_model=schemas.StudyGroup)
def schedule_meeting(
    group_id: int, schedule: schemas.ScheduleCreate, db: Session = Depends(get_db)
):
    db_study_group = crud.get_study_group(db, study_group_id=group_id)
    if db_study_group is None:
        raise HTTPException(status_code=404, detail="Study group not found")

    db_study_group.meeting_time = schedule.meeting_time
    db.commit()
    db.refresh(db_study_group)
    return db_study_group

@app.post("/groups/{group_id}/location", response_model=schemas.StudyGroup)
def set_location(
    group_id: int, location: schemas.LocationCreate, db: Session = Depends(get_db)
):
    db_study_group = crud.get_study_group(db, study_group_id=group_id)
    if db_study_group is None:
        raise HTTPException(status_code=404, detail="Study group not found")

    db_study_group.location = location.location
    db.commit()
    db.refresh(db_study_group)
    return db_study_group

@app.get("/groups/{group_id}/map")
def get_map(group_id: int, db: Session = Depends(get_db)):
    db_study_group = crud.get_study_group(db, study_group_id=group_id)
    if db_study_group is None:
        raise HTTPException(status_code=404, detail="Study group not found")

    if not db_study_group.location:
        raise HTTPException(status_code=404, detail="Location not set")

    return {"map_url": integrations.create_google_maps_embed(db_study_group.location)}

@app.get("/groups/{group_id}/ics")
def get_ics(group_id: int, db: Session = Depends(get_db)):
    db_study_group = crud.get_study_group(db, study_group_id=group_id)
    if db_study_group is None:
        raise HTTPException(status_code=404, detail="Study group not found")

    if not db_study_group.meeting_time:
        raise HTTPException(status_code=404, detail="Meeting time not set")

    # This is a naive implementation. A more robust solution would be to use a proper date parsing library.
    dtstart = datetime.strptime(db_study_group.meeting_time, "%Y-%m-%d %H:%M:%S")
    dtend = dtstart + timedelta(hours=1)

    return {"ics_file": integrations.create_ics_file(db_study_group.name, dtstart, dtend)}

@app.post("/groups/{group_id}/remind")
def remind_group(group_id: int, db: Session = Depends(get_db)):
    db_study_group = crud.get_study_group(db, study_group_id=group_id)
    if db_study_group is None:
        raise HTTPException(status_code=404, detail="Study group not found")

    # In a real app, you'd fetch members' emails and send actual reminders
    integrations.send_reminder(
        to_email="group_members@example.com",
        subject=f"Reminder for {db_study_group.name}",
        body=f"Your study group {db_study_group.name} is meeting soon at {db_study_group.location} on {db_study_group.meeting_time}."
    )
    return {"message": "Reminder sent (placeholder)"}
