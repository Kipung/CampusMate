from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_schedule_overlap(user_schedule, group_schedule):
    """
    Calculates the overlap between two schedules.
    Schedules are represented as strings of 0s and 1s, where 1 means available.
    """
    overlap = 0
    for i in range(len(user_schedule)):
        if user_schedule[i] == '1' and group_schedule[i] == '1':
            overlap += 1
    return overlap

def get_recommendations(user_study_habits, all_study_groups_habits, user_schedule, all_study_groups_schedules):
    """
    Calculates cosine similarity between a user's study habits and all study groups' habits,
    and also considers schedule overlap.

    Args:
        user_study_habits (str): A string of the user's study habits.
        all_study_groups_habits (list): A list of strings, where each string is the study habits of a study group.
        user_schedule (str): A string representing the user's schedule.
        all_study_groups_schedules (list): A list of strings, where each string is the schedule of a study group.

    Returns:
        A list of tuples, where each tuple contains the index of the study group and the combined score.
    """

    vectorizer = TfidfVectorizer()
    all_habits = [user_study_habits] + all_study_groups_habits
    tfidf_matrix = vectorizer.fit_transform(all_habits)
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])

    combined_scores = []
    for i, sim_score in enumerate(cosine_sim[0]):
        schedule_overlap = calculate_schedule_overlap(user_schedule, all_study_groups_schedules[i])
        # You can adjust the weighting of these two scores
        combined_score = sim_score + (schedule_overlap * 0.1) # Example weighting
        combined_scores.append((i, combined_score))

    return sorted(combined_scores, key=lambda x: x[1], reverse=True)
