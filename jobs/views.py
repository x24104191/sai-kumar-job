from django.shortcuts import render, redirect
import csv

# CSV files
USER_CSV = "users.csv"
JOB_CSV = "jobs.csv"
APPLICATION_CSV = "applications.csv"

# User Class (for managing users)
class User:
    def __init__(self, username, email, password, role):
        self.username = username
        self.email = email
        self.password = password
        self.role = role

    def save(self):
        with open(USER_CSV, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([self.username, self.email, self.password, self.role])

    @staticmethod
    def authenticate(email, password):
        try:
            with open(USER_CSV, "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[1] == email and row[2] == password:
                        return User(row[0], row[1], row[2], row[3])
        except FileNotFoundError:
            pass
        return None

# Job Class (for managing jobs)
class Job:
    def __init__(self, job_id, title, description, employer_email):
        self.id = job_id
        self.title = title
        self.description = description
        self.employer_email = employer_email

    def save(self):
        with open(JOB_CSV, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([self.id, self.title, self.description, self.employer_email])

    @staticmethod
    def get_all():
        jobs = []
        try:
            with open(JOB_CSV, "r") as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    jobs.append(Job(row[0], row[1], row[2], row[3]))
        except FileNotFoundError:
            pass
        return jobs

    @staticmethod
    def delete(job_id):
        jobs = Job.get_all()
        with open(JOB_CSV, "w", newline="") as file:
            writer = csv.writer(file)
            for job in jobs:
                if job.id != job_id:
                    writer.writerow([job.id, job.title, job.description, job.employer_email])

# Signup View
def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        role = request.POST["role"]

        user = User(username, email, password, role)
        user.save()
        return redirect("login")

    return render(request, "signup.html")

# Login View
def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = User.authenticate(email, password)
        if user:
            request.session["user_email"] = user.email
            request.session["role"] = user.role
            return redirect("dashboard")

    return render(request, "login.html")

# Logout View
def logout(request):
    request.session.flush()
    return redirect("login")

# Dashboard View (Redirects based on role)
def dashboard(request):
    if "user_email" not in request.session:
        return redirect("login")

    notification = request.session.pop("notification", None)

    user_role = request.session.get("role")
    if user_role == "Employer":
        return employer_dashboard(request)
    else:
        return job_list(request)

#
# Employer Dashboard
def employer_dashboard(request):
    if "user_email" not in request.session or request.session["role"] != "Employer":
        return redirect("login")

    jobs = [job for job in Job.get_all() if job.employer_email == request.session["user_email"]]
    return render(request, "employer_dashboard.html", {"jobs": jobs})

def employer_dashboard1(request):
    return render(request, 'employer_dashboard.html')

# Add Job View
def add_job(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        job_id = str(len(Job.get_all()) + 1)
        employer_email = request.session["user_email"]

        job = Job(job_id, title, description, employer_email)
        job.save()
        return redirect("dashboard")

    return render(request, "add_job.html")

# Delete Job View
def delete_job(request, job_id):
    Job.delete(job_id)
    return redirect("dashboard")



# Job Seeker Dashboard (View Jobs)
def job_list(request):
    if "user_email" not in request.session or request.session["role"] != "Job Seeker":
        return redirect("login")

    jobs = Job.get_all()
    applied_jobs = set()

    try:
        with open(APPLICATION_CSV, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == request.session["user_email"]:
                    applied_jobs.add(row[1])  # job.id
    except FileNotFoundError:
        pass
    return render(request, "jobseeker_dashboard.html", {"jobs": jobs, "applied_jobs": applied_jobs})



# Apply for a Job View
def apply_job(request, job_id):
    if "user_email" not in request.session or request.session["role"] != "Job Seeker":
        return redirect("login")

    applied_jobs = set()
    try:
        with open(APPLICATION_CSV, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == request.session["user_email"]:
                    applied_jobs.add(row[1])
    except FileNotFoundError:
        pass
    if job_id in applied_jobs:
        return redirect("dashboard")  # Prevent duplicate application

    with open(APPLICATION_CSV, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([request.session["user_email"], job_id, "Pending"])

    return redirect("dashboard")


# Review Applications (Employer)
def review_applications(request, job_id):
    if "user_email" not in request.session or request.session["role"] != "Employer":
        return redirect("login")

    applications = []
    try:
        with open(APPLICATION_CSV, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[1] == job_id:
                    applications.append({"email": row[0], "status": row[2]})
    except FileNotFoundError:
        pass
    return render(request, "review_applications.html", {"applications": applications, "job_id": job_id})


# Update Application Status (Employer decision)
def update_status(request, email, job_id, status):
    applications = []
    try:
        with open(APPLICATION_CSV, "r") as file:
            reader = csv.reader(file)
            applications = [row for row in reader]
    except FileNotFoundError:
        pass
    with open(APPLICATION_CSV, "w", newline="") as file:
        writer = csv.writer(file)
        for row in applications:
            if row[0] == email and row[1] == job_id:
                writer.writerow([email, job_id, status])
            else:
                writer.writerow(row)

    # Store notification in session
    request.session["notification"] = f"Your application for Job ID {job_id} has been {status.lower()}."

    return redirect("dashboard")
