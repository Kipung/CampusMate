from sqlalchemy.orm import Session

import models
import schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, email=user.email, study_habits=user.study_habits, schedule=user.schedule)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_study_group(db: Session, study_group_id: int):
    return db.query(models.StudyGroup).filter(models.StudyGroup.id == study_group_id).first()


def get_study_groups(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.StudyGroup).offset(skip).limit(limit).all()


def create_study_group(db: Session, study_group: schemas.StudyGroupCreate):
    db_study_group = models.StudyGroup(name=study_group.name, study_habits=study_group.study_habits, meeting_time=study_group.meeting_time, location=study_group.location, schedule=study_group.schedule)
    db.add(db_study_group)
    db.commit()
    db.refresh(db_study_group)
    return db_study_group
