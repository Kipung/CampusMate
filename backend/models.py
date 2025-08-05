from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    study_habits = Column(String)
    schedule = Column(String)

    enrollments = relationship("Enrollment", back_populates="user")
    memberships = relationship("Membership", back_populates="user")

class Class(Base):
    __tablename__ = 'classes'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    course_code = Column(String, unique=True)

    enrollments = relationship("Enrollment", back_populates="class_")

class Enrollment(Base):
    __tablename__ = 'enrollments'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    class_id = Column(Integer, ForeignKey('classes.id'))

    user = relationship("User", back_populates="enrollments")
    class_ = relationship("Class", back_populates="enrollments")

class StudyGroup(Base):
    __tablename__ = 'study_groups'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    study_habits = Column(String)
    schedule = Column(String)
    meeting_time = Column(String)
    location = Column(String)

    memberships = relationship("Membership", back_populates="study_group")

class Membership(Base):
    __tablename__ = 'memberships'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    study_group_id = Column(Integer, ForeignKey('study_groups.id'))

    user = relationship("User", back_populates="memberships")
    study_group = relationship("StudyGroup", back_populates="memberships")
