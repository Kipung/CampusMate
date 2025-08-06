import requests
import os
import time
import csv


BASE_URL = "http://backend:8000" # Use the service name 'backend' for inter-container communication

def run_test(test_name, func):
    print(f"--- Running Test: {test_name} ---")
    try:
        func()
        print(f"--- Test Succeeded: {test_name} ---\n")
        return True
    except Exception as e:
        print(f"--- Test Failed: {test_name} ---")
        print(f"Error: {e}\n")
        return False

def test_health_checks():
    response = requests.get(f"{BASE_URL}/healthz")
    response.raise_for_status()
    assert response.json() == {"status": "ok"}

    response = requests.get(f"{BASE_URL}/healthcheck")
    response.raise_for_status()
    assert response.json() == {"status": "ok"}

def test_user_management():
    # Create user
    user_data = {
        "name": "Test User",
        "email": "testuser@example.com",
        "study_habits": "likes to study alone",
        "schedule": "111100001111000011110000"
    }
    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    response.raise_for_status()
    created_user = response.json()
    assert created_user["name"] == user_data["name"]
    assert created_user["email"] == user_data["email"]
    assert created_user["study_habits"] == user_data["study_habits"]
    assert created_user["schedule"] == user_data["schedule"]
    print(f"Created user: {created_user['id']}")

    # Get all users
    response = requests.get(f"{BASE_URL}/users/")
    response.raise_for_status()
    users = response.json()
    assert any(u["id"] == created_user["id"] for u in users)
    print(f"Retrieved all users. Found {len(users)} users.")

    # Get specific user
    response = requests.get(f"{BASE_URL}/users/{created_user['id']}")
    response.raise_for_status()
    retrieved_user = response.json()
    assert retrieved_user["id"] == created_user["id"]
    print(f"Retrieved specific user: {retrieved_user['id']}")

def test_study_group_management():
    # Create study group
    study_group_data = {
        "name": "Test Study Group",
        "study_habits": "prefers group discussions",
        "schedule": "000011110000111100001111",
        "meeting_time": "2025-08-10 14:00:00",
        "location": "University Library"
    }
    response = requests.post(f"{BASE_URL}/study_groups/", json=study_group_data)
    response.raise_for_status()
    created_group = response.json()
    assert created_group["name"] == study_group_data["name"]
    print(f"Created study group: {created_group['id']}")

    # Get all study groups
    response = requests.get(f"{BASE_URL}/study_groups/")
    response.raise_for_status()
    study_groups = response.json()
    assert any(g["id"] == created_group["id"] for g in study_groups)
    print(f"Retrieved all study groups. Found {len(study_groups)} groups.")

    # Get specific study group
    response = requests.get(f"{BASE_URL}/study_groups/{created_group['id']}")
    response.raise_for_status()
    retrieved_group = response.json()
    assert retrieved_group["id"] == created_group["id"]
    print(f"Retrieved specific study group: {retrieved_group['id']}")

def test_matching_engine():
    # Ensure there's at least one user and one study group for matching
    user_data = {
        "name": "Matcher User",
        "email": "matcher@example.com",
        "study_habits": "likes to study alone",
        "schedule": "111100001111000011110000"
    }
    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    response.raise_for_status()
    matcher_user = response.json()

    study_group_data = {
        "name": "Matcher Group",
        "study_habits": "prefers group discussions",
        "schedule": "000011110000111100001111",
        "meeting_time": "2025-08-10 14:00:00",
        "location": "University Library"
    }
    response = requests.post(f"{BASE_URL}/study_groups/", json=study_group_data)
    response.raise_for_status()
    response.json() # Assigned to but never used, removed assignment

    response = requests.post(f"{BASE_URL}/match", params={"user_id": matcher_user["id"]})
    response.raise_for_status()
    recommendations = response.json()
    assert isinstance(recommendations, list)
    print(f"Received {len(recommendations)} recommendations.")

def test_in_person_features():
    # Create a study group to test with
    study_group_data = {
        "name": "In-Person Test Group",
        "study_habits": "flexible",
        "schedule": "111111111111111111111111",
        "meeting_time": "2025-08-15 10:00:00",
        "location": "Campus Cafe"
    }
    response = requests.post(f"{BASE_URL}/study_groups/", json=study_group_data)
    response.raise_for_status()
    test_group = response.json()

    # Test schedule update
    new_schedule_data = {"meeting_time": "2025-08-16 11:00:00"}
    response = requests.post(f"{BASE_URL}/groups/{test_group['id']}/schedule", json=new_schedule_data)
    response.raise_for_status()
    updated_group = response.json()
    assert updated_group["meeting_time"] == new_schedule_data["meeting_time"]
    print(f"Updated group schedule: {updated_group['meeting_time']}")

    # Test location update
    new_location_data = {"location": "Student Union"}
    response = requests.post(f"{BASE_URL}/groups/{test_group['id']}/location", json=new_location_data)
    response.raise_for_status()
    updated_group = response.json()
    assert updated_group["location"] == new_location_data["location"]
    print(f"Updated group location: {updated_group['location']}")

    # Test map URL
    response = requests.get(f"{BASE_URL}/groups/{test_group['id']}/map")
    response.raise_for_status()
    map_data = response.json()
    assert "map_url" in map_data
    assert "https://maps.google.com/maps?q=" in map_data["map_url"] # Check for mocked URL
    print(f"Retrieved map URL: {map_data['map_url']}")

    # Test ICS file
    response = requests.get(f"{BASE_URL}/groups/{test_group['id']}/ics")
    response.raise_for_status()
    ics_data = response.json()
    assert "ics_file" in ics_data
    assert "BEGIN:VCALENDAR" in ics_data["ics_file"]
    print("Retrieved ICS file content.")

    # Test reminder (check backend logs for output)
    response = requests.post(f"{BASE_URL}/groups/{test_group['id']}/remind")
    response.raise_for_status()
    reminder_data = response.json()
    assert reminder_data["message"] == "Reminder sent (placeholder)"
    print(f"Reminder endpoint triggered: {reminder_data['message']}")

def test_data_export():
    # Trigger export script
    print("Triggering data export...")
    # This command runs the export script directly inside the container
    # We cannot capture its stdout/stderr directly here, but we can check the file
    os.system("PYTHONPATH=/app python scripts/export.py") 
    
    export_file_path = "/data/exports/export.csv"
    
    # Wait a moment for the file to be written
    time.sleep(2) 

    if not os.path.exists(export_file_path):
        raise FileNotFoundError(f"Export file not found at {export_file_path}")

    with open(export_file_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        assert header == ['user_id', 'user_study_habits', 'study_group_id', 'study_group_study_habits']
        rows = list(reader)
        assert len(rows) > 0 # Ensure some data was exported
        print(f"Exported {len(rows)} rows to {export_file_path}")

if __name__ == "__main__":
    results = []

    # Give services a moment to fully start up
    print("Giving services a moment to start...")
    time.sleep(10) 

    results.append(run_test("Health Checks", test_health_checks))
    results.append(run_test("User Management", test_user_management))
    results.append(run_test("Study Group Management", test_study_group_management))
    results.append(run_test("Matching Engine", test_matching_engine))
    results.append(run_test("In-Person Features", test_in_person_features))
    results.append(run_test("Data Export", test_data_export))

    print()
    print("--- Automated API and Data Export Test Summary ---")
    for success, test_name in zip(results, ["Health Checks", "User Management", "Study Group Management", "Matching Engine", "In-Person Features", "Data Export"]):
        status = "PASSED" if success else "FAILED"
        print(f"{test_name}: {status}")
    print("--------------------------------------------------")

    print()
    print("--- Running Automated Backend (Pytest) and Frontend (Lint) Checks ---")
    
