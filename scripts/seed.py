from sqlalchemy.orm import sessionmaker
from database import engine
from models import User, Class, Enrollment, StudyGroup, Membership

Session = sessionmaker(bind=engine)

def seed_data():
    session = Session()

    # Clear existing data
    session.query(Enrollment).delete()
    session.query(Membership).delete()
    session.query(User).delete()
    session.query(Class).delete()
    session.query(StudyGroup).delete()
    session.commit()

    # Create users
    user1 = User(name="Alice", email="alice@example.com", study_habits="prefers to study in the morning", schedule="111110000000000000000000")
    user2 = User(name="Bob", email="bob@example.com", study_habits="prefers to study in the evening", schedule="000000000000111110000000")

    # Create classes
    class1 = Class(name="Introduction to Python", course_code="CS101")
    class2 = Class(name="Data Structures and Algorithms", course_code="CS201")

    # Create enrollments
    enrollment1 = Enrollment(user=user1, class_=class1)
    enrollment2 = Enrollment(user=user2, class_=class2)

    # Create study groups
    study_group1 = StudyGroup(name="Python Beginners", study_habits="morning study group", schedule="111110000000000000000000")
    study_group2 = StudyGroup(name="Algo Experts", study_habits="evening study group", schedule="000000000000111110000000")

    # Create memberships
    membership1 = Membership(user=user1, study_group=study_group1)
    membership2 = Membership(user=user2, study_group=study_group2)

    session.add_all([user1, user2, class1, class2, enrollment1, enrollment2, study_group1, study_group2, membership1, membership2])
    session.commit()

    session.close()

if __name__ == "__main__":
    seed_data()