import pytest
from app2 import app, db, User, jobs
from flask import jsonify
from werkzeug.security import generate_password_hash

@pytest.fixture
def client():
    # Set up the Flask app and the test client
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_database.db'
    app.config['TESTING'] = True
    with app.test_client() as client:
        # Create the database tables
        with app.app_context():
            db.create_all()
        yield client
        # Clean up the database after the tests
        with app.app_context():
            db.drop_all()


# Integration Test for the full User Signup, Login, and Job Application flow
def test_user_signup_login_and_apply(client):
    # Step 1: Sign up a new user
    response = client.post('/userSignup', json={
        'username': 'testuser',
        'password': 'password123',
        'email': 'testuser@example.com',
        'fullname': 'Test User'
    })
    data = response.get_json()
    assert response.status_code == 201
    assert data['success'] is True
    assert data['message'] == 'User registered successfully'

    # Step 2: Log in with the new user's credentials
    response = client.post('/userLogin', json={
        'email': 'testuser@example.com',
        'password': 'password123'
    })
    data = response.get_json()
    assert response.status_code == 200
    assert data['success'] is True
    assert data['message'] == 'Logged in successfully'

    # Step 3: Add a job listing to the system
    job1 = jobs(jobId=1, jobTitle='Software Engineer', location='New York', experience='2-5 years', salaryRange='$1000-$2000')
    with app.app_context():
        db.session.add(job1)
        db.session.commit()

    # Step 4: Retrieve job listings and ensure the job is in the list
    response = client.get('/api/jobslist')
    data = response.get_json()
    assert response.status_code == 200
    assert len(data) > 0
    assert data[0]['jobTitle'] == 'Software Engineer'

    # Step 5: Apply to the job
    response = client.post('/apply/1', data={
        'email': 'testuser@example.com',
        'jobTitle': 'Software Engineer',
        'portfolio': 'https://myportfolio.com',
        'resume': 'resume.pdf'
    })
    data = response.get_json()
    assert response.status_code == 200
    assert data['success'] is True
    assert data['message'] == 'Application submitted successfully!'


# Integration Test for searching for jobs
def test_search_jobs_flow(client):
    # Step 1: Add jobs to the database
    job1 = jobs(jobId=1, jobTitle='Software Engineer', location='New York', experience='2-5 years', salaryRange='$1000-$2000')
    job2 = jobs(jobId=2, jobTitle='Data Scientist', location='San Francisco', experience='3-5 years', salaryRange='$3000-$4000')
    with app.app_context():
        db.session.add(job1)
        db.session.add(job2)
        db.session.commit()

    # Step 2: Search for jobs by keyword
    response = client.post('/api/searchjobs', json={
        'title_keyword': 'Engineer',
        'location': 'New York',
        'type': ['Full-Time'],
        'exp': ['2-5 years']
    })
    data = response.get_json()
    assert response.status_code == 200
    assert len(data) > 0
    assert data[0]['jobTitle'] == 'Software Engineer'


# Integration Test for profile settings and job application flow
def test_user_profile_and_job_application(client):
    # Step 1: Register and log in the user
    response = client.post('/userSignup', json={
        'username': 'testuser',
        'password': 'password123',
        'email': 'testuser@example.com',
        'fullname': 'Test User'
    })
    data = response.get_json()
    assert response.status_code == 201
    assert data['success'] is True
    assert data['message'] == 'User registered successfully'

    response = client.post('/userLogin', json={
        'email': 'testuser@example.com',
        'password': 'password123'
    })
    data = response.get_json()
    assert response.status_code == 200
    assert data['success'] is True
    assert data['message'] == 'Logged in successfully'

    # Step 2: Save profile settings
    response = client.post('/save-profile', json={
        'email': 'testuser@example.com',
        'mobile': '1234567890',
        'experience': '5 years',
        'education': 'Bachelor\'s in Computer Science',
        'age': 25,
        'gender': 'Male',
        'aboutMe': 'A passionate software developer.',
        'currentJob': 'Software Engineer',
        'hiEd': 'Bachelor\'s',
        'portfolio_url': 'https://myportfolio.com',
        'current_company': 'Tech Co.',
        'work_type': 'Full-time',
        'start_date': '2022-01-01',
        'current_location': 'New York',
        'job_description': 'Develop software solutions.',
        'recent_jobtitle': 'Junior Developer',
        'recent_company': 'Old Tech',
        'recent_worktype': 'Full-time',
        'recent_duration': '2 years',
        'recent_location': 'New York',
        'recent_jobdescription': 'Worked on web applications.',
        'institute': 'ABC University',
        'duration': '4 years',
        'course_description': 'Software Engineering',
        'skill1': 'Python',
        'skill2': 'Flask',
        'skill3': 'SQL',
        'skill4': 'Django',
        'skill5': 'JavaScript'
    })
    data = response.get_json()
    assert response.status_code == 200
    assert data['success'] is True
    assert data['message'] == 'Profile saved successfully!'

    # Step 3: Add a job listing and apply to it
    job1 = jobs(jobId=1, jobTitle='Software Engineer', location='New York', experience='2-5 years', salaryRange='$1000-$2000')
    with app.app_context():
        db.session.add(job1)
        db.session.commit()

    # Step 4: Apply to the job
    response = client.post('/apply/1', data={
        'email': 'testuser@example.com',
        'jobTitle': 'Software Engineer',
        'portfolio': 'https://myportfolio.com',
        'resume': 'resume.pdf'
    })
    data = response.get_json()
    assert response.status_code == 200
    assert data['success'] is True
    assert data['message'] == 'Application submitted successfully!'


# Integration Test for User Registration and Duplicate Username Error
def test_user_signup_duplicate_username(client):
    # Step 1: Sign up the first user
    response = client.post('/userSignup', json={
        'username': 'testuser',
        'password': 'password123',
        'email': 'testuser@example.com',
        'fullname': 'Test User'
    })
    data = response.get_json()
    assert response.status_code == 201
    assert data['success'] is True
    assert data['message'] == 'User registered successfully'

    # Step 2: Attempt to sign up with the same username
    response = client.post('/userSignup', json={
        'username': 'testuser',
        'password': 'password456',
        'email': 'testuser2@example.com',
        'fullname': 'Test User 2'
    })
    data = response.get_json()
    assert response.status_code == 400
    assert data['error'] == 'Username already exists'
