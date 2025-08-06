import csv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import User, StudyGroup


def export_data():
    """
    Exports anonymized user and study group data to a CSV file.
    """
    if not os.path.exists('/data/exports'):
        os.makedirs('/data/exports')

    engine = create_engine("postgresql://user:password@postgres/campusmate")
    Session = sessionmaker(bind=engine)
    session = Session()

    users = session.query(User).all()
    study_groups = session.query(StudyGroup).all()

    with open('/data/exports/export.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['user_id', 'user_study_habits', 'study_group_id', 'study_group_study_habits'])
        for user in users:
            for study_group in study_groups:
                writer.writerow([user.id, user.study_habits, study_group.id, study_group.study_habits])

if __name__ == '__main__':
    export_data()