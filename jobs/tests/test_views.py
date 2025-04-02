import pytest
import csv
from jobs.views import User, Job  # Import your classes

@pytest.fixture
def temp_user_csv(tmp_path):
    """Creates a temporary CSV file for user data."""
    temp_file = tmp_path / "users.csv"
    with temp_file.open("w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["testuser", "test@example.com", "securepass", "jobseeker"])
    return temp_file

@pytest.fixture
def temp_job_csv(tmp_path):
    """Creates a temporary CSV file for job data."""
    temp_file = tmp_path / "jobs.csv"
    with temp_file.open("w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["1", "Software Engineer", "Develop applications", "employer@example.com"])
    return temp_file

def test_user_authentication(temp_user_csv, monkeypatch):
    """Test if user authentication works correctly."""
    
    # Monkeypatch the CSV file path
    monkeypatch.setattr("jobs.views.USER_CSV", str(temp_user_csv))
    
    # Authenticate the user
    user = User.authenticate("test@example.com", "securepass")
    
    assert user is not None
    assert user.username == "testuser"
    assert user.role == "jobseeker"

def test_user_signup(temp_user_csv, monkeypatch):
    """Test if a new user can sign up successfully."""
    
    monkeypatch.setattr("jobs.views.USER_CSV", str(temp_user_csv))
    
    new_user = User("newuser", "new@example.com", "newpass", "employer")
    new_user.save()
    
    with temp_user_csv.open("r") as file:
        reader = list(csv.reader(file))
    
    assert len(reader) == 2  # New user should be added

def test_job_save(temp_job_csv, monkeypatch):
    """Test if a job is saved correctly."""
    
    monkeypatch.setattr("jobs.views.JOB_CSV", str(temp_job_csv))
    
    new_job = Job("2", "Data Scientist", "Analyze data", "data@example.com")
    new_job.save()
    
    with temp_job_csv.open("r") as file:
        reader = list(csv.reader(file))
    
    assert len(reader) == 2  # New job should be added


def test_delete_job(temp_job_csv, monkeypatch):
    """Test job deletion."""
    
    monkeypatch.setattr("jobs.views.JOB_CSV", str(temp_job_csv))
    
    Job.delete("1")  # Delete existing job
    
    with temp_job_csv.open("r") as file:
        reader = list(csv.reader(file))
    
    assert len(reader) == 0  # Job should be deleted
