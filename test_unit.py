import pytest
from app2 import app, db, User, jobs, Application
from flask import jsonify

# Set up the test client and database
@pytest.fixture
def client():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_database.db'
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

# Test company signup route
def test_company_signup(client):
    with app.app_context():
        # Valid signup
        response = client.post('/companysignup', json={
            'username': 'testcompany',
            'password': 'password123',
            'email': 'testcompany@example.com',
            'fullname': 'Test Company',
            'is_recruiter': True
        })
        data = response.get_json()
        assert response.status_code == 201
        assert data['success'] is True
        assert data['message'] == 'User registered successfully'

        # Test company with existing username
        response = client.post('/companysignup', json={
            'username': 'testcompany',
            'password': 'password123',
            'email': 'newcompany@example.com',
            'fullname': 'New Company',
            'is_recruiter': True
        })
        data = response.get_json()
        assert response.status_code == 400
        assert data['error'] == 'Username already exists'

# Test company login route
def test_company_login(client):
    with app.app_context():
        # Register a company
        client.post('/companysignup', json={
            'username': 'testcompany',
            'password': 'password123',
            'email': 'testcompany@example.com',
            'fullname': 'Test Company',
            'is_recruiter': True
        })
        
        # Login route test
        response = client.post('/companylogin', json={
            'email': 'testcompany@example.com',
            'password': 'password123'
        })
        data = response.get_json()
        assert response.status_code == 200
        assert data['success'] is True
        assert data['message'] == 'Logged in successfully'

# Test company profile route
def test_company_profile(client):
    with app.app_context():
        # Register and login the company
        client.post('/companysignup', json={
            'username': 'testcompany',
            'password': 'password123',
            'email': 'testcompany@example.com',
            'fullname': 'Test Company',
            'is_recruiter': True
        })
        client.post('/companylogin', json={
            'email': 'testcompany@example.com',
            'password': 'password123'
        })

        # Add job to the database
        job1 = jobs(jobId=1, jobTitle='Software Engineer', companyName='Test Company', location='New York', experience='2-5 years', salaryRange='$1000-$2000')
        db.session.add(job1)
        db.session.commit()

        # Test the company profile endpoint
        response = client.get('/company-profile')
        data = response.get_json()
        assert response.status_code == 200
        assert data[0]['fullname'] == 'Test Company'
        assert data[0]['jobTitle'] == 'Software Engineer'

# Test company applicants list route
def test_company_applicants_list(client):
    with app.app_context():
        # Register and login the company
        client.post('/companysignup', json={
            'username': 'testcompany',
            'password': 'password123',
            'email': 'testcompany@example.com',
            'fullname': 'Test Company',
            'is_recruiter': True
        })
        client.post('/companylogin', json={
            'email': 'testcompany@example.com',
            'password': 'password123'
        })

        # Add a job
        job1 = jobs(jobId=1, jobTitle='Software Engineer', companyName='Test Company', location='New York', experience='2-5 years', salaryRange='$1000-$2000')
        db.session.add(job1)
        db.session.commit()

        # Register a user and apply for the job
        client.post('/userSignup', json={
            'username': 'testuser',
            'password': 'password123',
            'email': 'testuser@example.com',
            'fullname': 'Test User'
        })
        client.post('/userLogin', json={
            'email': 'testuser@example.com',
            'password': 'password123'
        })
        client.post('/apply/1', data={
            'email': 'testuser@example.com',
            'jobTitle': 'Software Engineer',
            'portfolio': 'https://myportfolio.com',
            'resume': 'resume.pdf'
        })

        # Test applicants list
        response = client.get('/applicantslist?jobTitle=Software Engineer')
        data = response.get_json()
        assert response.status_code == 200
        assert len(data['applicants']) > 0
        assert data['applicants'][0]['fullname'] == 'Test User'

# Test company logout route
def test_company_logout(client):
    with app.app_context():
        # Register and login the company
        client.post('/companysignup', json={
            'username': 'testcompany',
            'password': 'password123',
            'email': 'testcompany@example.com',
            'fullname': 'Test Company',
            'is_recruiter': True
        })
        client.post('/companylogin', json={
            'email': 'testcompany@example.com',
            'password': 'password123'
        })

        # Test company logout
        response = client.get('/companylogout')
        assert response.status_code == 200
        assert 'company_login.html' in response.data.decode()

