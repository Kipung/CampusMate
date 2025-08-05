from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    email: str
    study_habits: str
    schedule: str | None = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class StudyGroupBase(BaseModel):
    name: str
    study_habits: str
    schedule: str | None = None
    meeting_time: str | None = None
    location: str | None = None

class StudyGroupCreate(StudyGroupBase):
    pass

class StudyGroup(StudyGroupBase):
    id: int

    class Config:
        orm_mode = True

class ScheduleCreate(BaseModel):
    meeting_time: str

class LocationCreate(BaseModel):
    location: str
