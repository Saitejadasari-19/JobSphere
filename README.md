# JobSphere: A Flask Job Portal

## Description

JobSphere is a web application built with Flask that serves as a platform for job seekers and companies to connect. Job seekers can browse available jobs, apply to positions, and manage their profiles. Companies can post job listings and manage applications.

## Features

The current features include:

*   User registration and login
*   Company/Recruiter registration and login
*   Displaying job listings with filtering and search capabilities
*   Viewing individual job details
*   Applying to jobs
*   User profile creation and viewing
*   Company profile viewing (listing their jobs and applicant counts)
*   Viewing a list of applicants for a specific job
*   Viewing recent applications for a user
*   Basic handling of static files (CSS, HTML)

## Technical Stack

*   **Backend Framework:** Flask (Python)
*   **Database:** SQLite (using SQLAlchemy ORM)
*   **Frontend:** HTML, CSS, JavaScript (served as static files)
*   **Password Hashing:** Werkzeug Security

## Installation

1.  **Clone the repository:**
```
bash
    git clone <repository_url>
    cd JobSphere
    
```
2.  **Create a virtual environment:**
```
bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    
```
3.  **Install dependencies:**
```
bash
    pip install -r requirements.txt
    
```


## Database Setup

The application uses an SQLite database. Upon the first run, SQLAlchemy will create the `database.db` file in the `database` directory (which you may need to create if it doesn't exist: `mkdir database`).


## How to Run the Application

1.  Ensure you are in the project's root directory (`JobSphere`).
2.  Activate your virtual environment:
```
bash
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    
```
3.  Run the Flask application:
```
bash
    python app.py
    
```
4.  Open your web browser and go to `http://127.0.0.1:5000/`.

## Future Improvements

Here are some planned features to enhance JobSphere:

*   **Pagination:** Implement pagination for job listings and applicant lists for better performance.
*   **Resume Upload and Parsing:** Allow users to upload resumes and automatically extract information.
*   **Skill Matching:** Develop a system to match user skills with job requirements and suggest relevant jobs.
*   **Job Recommendations:** Implement a job recommendation engine based on user activity and profile.
*   **Input Validation:** Enhance input validation on all forms and API endpoints.
*   **Improved Error Handling:** Provide more specific and user-friendly error messages.
*   **Testing:** Add unit and integration tests for core functionalities.
*   **Deployment:** Prepare the application for deployment on a cloud platform.
*   **Containerization:** Containerize the application using Docker.
*   **CI/CD:** Set up a Continuous Integration/Continuous Deployment pipeline.
*   **Job Posting:** Implement a feature for companies to create new job listings.
*   **Edit/Delete Jobs:** Allow companies to manage their job postings.
*   **User Profile Editing:** Enable users to edit their profile details.
*   **Job Application Management (Company):** Provide tools for companies to manage applications and update statuses.
*   **Job Application Withdrawal (User):** Allow users to withdraw applications.
*   **More Advanced Search and Filtering:** Add more criteria for searching and filtering jobs.
*   **Email Notifications:** Implement email notifications for application status updates and new applications.
*   **Admin Panel:** Create an interface for administrative tasks.
*   **API Documentation:** Generate documentation for the application's API endpoints.
