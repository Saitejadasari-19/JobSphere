from flask import Flask,send_from_directory, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
import base64

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/database.db'
app.secret_key = 'ItsaSecret'
db = SQLAlchemy(app)

@app.route('/userSignup', methods=['GET','POST'])
def usersignup():
    if request.args.get('view') == 'html':
        return send_from_directory('static','user_signup.html')
    else:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        fullname = data.get('fullname')

        if User.query.filter_by(userId=username).first():
            return jsonify({'error': 'Username already exists'}), 400

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8 )
        new_user = User(userId=username, fullname=fullname, password=hashed_password, email=email, is_recruiter=False)
        db.session.add(new_user)
        db.session.commit()
        session['userId'] = username
        session['fullname'] = fullname
        session['email'] = email
        return jsonify({'success':True,'message': 'User registered successfully'}), 201

@app.route('/companysignup', methods=['POST','GET'])
def companysignup():

    if request.args.get('view') == 'html':
        return send_from_directory('static','company_signup.html')
    
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    fullname = data.get('fullname')

    if User.query.filter_by(userId=username).first():
        return jsonify({'error': 'Username already exists'}), 400

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
    new_user = User(userId=username, password=hashed_password, email=email, fullname=fullname, is_recruiter=True)
    db.session.add(new_user)
    db.session.commit()
    session['userId'] = username
    session['fullname'] = fullname
    session['email'] = email
    return jsonify({'success':True,'message': 'User registered successfully'}), 201


@app.route('/userLogin',methods=['GET','POST'])
def userlogin():
    if request.args.get('view') == 'html':
        return send_from_directory('static','user_login.html')
    else:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        user = User.query.filter_by(email=email).first()
        if user.is_recruiter or not check_password_hash(user.password, password):
            return jsonify({'error': 'Invalid username or password'}), 401
        session['userId'] = user.userId
        session['fullname'] = user.fullname
        session['email'] = user.email
        return jsonify({'success':True, 'id': user.userId ,'message': 'Logged in successfully'}), 200

@app.route('/companylogin',methods=['POST','GET'])
def companylogin():
    if request.args.get('view') == 'html':
        return send_from_directory('static','company_login.html')
    data = request.json
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()
    if not user.is_recruiter or not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid username or password'}), 401
    session['userId'] = user.userId
    session['fullname'] = user.fullname
    session['email'] = user.email
    return jsonify({'success':True,'message': 'Logged in successfully'}), 200

#for css files
@app.route('/<path:folder>/<path:filename>')
def send_css(folder,filename):
    return send_from_directory(os.path.join(app.static_folder, folder), filename)
    
@app.route('/apply/<int:job_id>',methods=['GET'])
def apply(job_id):
    return send_from_directory('static','user_apply.html')

@app.route('/')
def home():
    return send_from_directory('static','user_login.html')

@app.route('/jobs')
def joblist():
    return send_from_directory('static','user_joblisting.html')

#userHome page
@app.route('/userhome')
def userHome():
    if request.args.get('view') == 'html':
        return send_from_directory('static','user_home.html')

#companyProfile page
@app.route('/companyhome',methods=['GET'])
def companyhome():
    if request.args.get('view') == 'html':
        return send_from_directory('static','company_profile.html')
    
@app.route('/userprofile', methods=['GET'])
def userprofile():
    return send_from_directory('static','user_profile.html')

@app.route('/dashboard',methods=['GET'])
def dashboard():
    if request.args.get('view') == 'html':
        return send_from_directory('static','user_dashboard.html')

@app.route('/settings',methods=['GET'])
def settings():
    if request.args.get('view') == 'html':
        return send_from_directory('static','user_setting.html')
    
@app.route('/companyapplicantlist',methods=['GET'])
def companyApplicantlist():
    if request.args.get('view') == 'html':
        return send_from_directory('static','company_applicantslist.html')
    
@app.route('/userLogout',methods=['GET'])
def userlogout():
    session.clear()
    return send_from_directory('static','user_login.html')
@app.route('/companylogout',methods=['GET'])
def companylogout():
    session.clear()
    return send_from_directory('static','company_login.html')

@app.route('/applicantprofile/<username>',methods=['GET'])
def applicantprofile(username):

    return send_from_directory('static','company_applicantprofile.html')

@app.route('/apply/api/<int:job_id>', methods=['GET'])
def get_job(job_id):
    job = jobs.query.filter_by(jobId=job_id).first()
    if not job:
        return jsonify({"error": "Job not found"}), 404
    return jsonify(job.to_dict())

@app.route('/apply/<int:job_id>', methods=['POST'])
def apply_to_job(job_id):
    email = request.form.get('email')
    job_title = request.form.get('jobTitle')
    portfolio = request.form.get('portfolio')
    resume = request.files.get('resume')
    user = User.query.filter_by(email=email).first()
    userId = user.userId
    applicant = Application(userId=userId, jobId=job_id, portfolio=portfolio, status="In Review")
    db.session.add(applicant)
    db.session.commit()
    return jsonify({"success": True, "message": "Application submitted successfully!"}), 200

@app.route('/usersettingsname')
def usersettingsname():
    fullname = session['fullname']
    email = session['email']
    return jsonify({'fullname':fullname,'email':email})

#for user joblisting
@app.route('/api/jobslist', methods=['GET'])
def jobslist():
    # Retrieve filter parameters from the request
    title_keyword = request.args.get('title', '').strip()
    location = request.args.get('location', '').strip()
    employment_type = request.args.getlist('type')
    exp = request.args.getlist('exp')  
    # Fetch filtered jobs based on the parameters
    filtered_jobs_query = db.session.query(jobs)
    if title_keyword:
        filtered_jobs_query = filtered_jobs_query.filter(jobs.jobTitle.ilike(f'%{title_keyword}%'))
    # Filter by location if provided
    if location:
        filtered_jobs_query = filtered_jobs_query.filter(jobs.location.ilike(f'%{location}%'))
    # Add filters based on the filter inputs
    if employment_type:
        filtered_jobs_query = filtered_jobs_query.filter(jobs.workType.in_(employment_type))
    if exp:
        filtered_jobs_query = filtered_jobs_query.filter(jobs.experience.in_(exp))
    # Execute the query to get the filtered jobs
    filtered_jobs = filtered_jobs_query.limit(10)
    jobs_list = [j.to_dict() for j in filtered_jobs]
    return jsonify(jobs_list)

#For applicant status
@app.route('/status/<st>/<username>', methods=['POST'])
def status(st, username):
    applicant = Application.query.filter_by(userId=username).first()
    # Check if the applicant exists
    if not applicant:
        return jsonify({"success": False, "message": "Applicant not found"}), 404
    # Update the applicant's status
    applicant.status = st
    db.session.commit()
    return jsonify({"success": True, "message": "Status updated!"})

#for user job listings(search)
@app.route('/api/searchjobs', methods=['POST'])
def search_jobs():
    title_keyword = request.form.get('title_keyword')
    location = request.form.get('location')
    employment_type = request.form.getlist('type')
    exp = request.form.getlist('exp')
    # Fetch filtered jobs based on the parameters
    filtered_jobs_query = db.session.query(jobs)
    # Add filters based on the filter inputs
    if employment_type:
        filtered_jobs_query = filtered_jobs_query.filter(jobs.workType.in_(employment_type))
    if exp:
        filtered_jobs_query = filtered_jobs_query.filter(jobs.experience.in_(exp))
    # Filter by title or keyword if provided
    if title_keyword:
        filtered_jobs_query = filtered_jobs_query.filter(jobs.jobTitle.ilike(f'%{title_keyword}%'))
    # Filter by location if provided
    if location:
        filtered_jobs_query = filtered_jobs_query.filter(jobs.location.ilike(f'%{location}%'))
    # Execute the query and fetch results
    filtered_jobs = filtered_jobs_query.limit(10)
    # Convert to JSON-serializable format
    jobs_list = [job.to_dict() for job in filtered_jobs]  # Ensure to_dict() is implemented in jobs model
    return jsonify(jobs_list)

#For Job Listings
@app.route('/showjobs',methods=['GET'])
def showjobs():
    job = jobs.query.limit(10)
    jobs_list = [j.to_dict() for j in job]
    return jsonify(jobs_list)

@app.route('/company-profile', methods=['GET'])
def company_profile():
    # Get the recruiter (company) details from the 'users' table
    fullname = session['fullname']
    if fullname:
        # Get job listings for the company from the 'jobs' table where companyname matches fullname
        jobs_data = jobs.query.filter_by(companyName=fullname).all()

        if jobs_data:
            job = jobs_data[0]
            company_details = {
                'fullname': job.companyName,
                'size': job.companySize,
                'location': job.location,
                'email1': job.contact,
                'benefits': job.benefits[2:-2].split(","),
                'profile' : job.companyProfile,
                'jobTitle' : job.jobTitle,
                'worktype' : job.workType
                #job post date is null, can be added similarly
            }
            # Return the company details as a JSON response
            return jsonify(company_details)
        else:
            return jsonify({"error": "No jobs found for this company."}), 404
    else:
        return jsonify({"error": "Company not found."}), 404

#for applicantslist
@app.route('/applicantslist', methods=['GET'])
def applicants_list():
    # Get company details from session
    fullname = session['fullname']
    if not fullname:
        return jsonify({"error": "Company not found."}), 404

    # Fetch the jobId based on the company name and job title from session data or frontend
    job_title = request.args.get('jobTitle')  # You can pass jobTitle as a query parameter
    job = jobs.query.filter_by(companyName=fullname, jobTitle=job_title).first()
    if not job:
        return jsonify({"error": "Job not found."}), 404

    # Fetch applicants for the given job
    applicants = Application.query.filter_by(jobId=job.jobId).all()

    # Prepare the list of applicants with status and user information
    applicant_list = []
    for application in applicants:
        user = User.query.filter_by(userId=application.userId).first()
        if user:
            applicant_info = {
                'fullname': user.fullname,
                'status': application.status,
                'portfolio': application.portfolio  # Add other fields if needed
            }
            applicant_list.append(applicant_info)
    # Return job info and applicant list as JSON
    return jsonify({
        'companyName': job.companyName,
        'jobTitle': job.jobTitle,
        'workType': job.workType,
        'applicants': applicant_list
    })

#for user dashboard 
@app.route('/recent-applications', methods=['GET'])
def recent_applications():
    # Get userId from session (assumed that userId is stored in session upon login)
    user_id = session['userId']
    if not user_id:
        return jsonify({"error": "User not logged in."}), 401
    # Fetch applications for the current user
    applications_data = Application.query.filter_by(userId=user_id).all()
    if not applications_data:
        return jsonify({"message": "No applications found."}), 404
    applications_list = []
    for application in applications_data:
        # Get the job associated with this application
        job = jobs.query.filter_by(jobId=application.jobId).first()
        if job:
            application_details = {
                'jobTitle': job.jobTitle,
                'companyName': job.companyName,
                'location': job.location,
                'workType': job.workType,
                'status': application.status,              
            }
            applications_list.append(application_details)
    # Fetch user fullname for the "Good morning" greeting
    user = User.query.filter_by(userId=user_id).first()
    if not user:
        return jsonify({"error": "User not found."}), 404
    # Return the user's fullname and applications as JSON
    return jsonify({
        'fullname': user.fullname,
        'applications': applications_list
    })

#for user home
@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    id = session['userId']
    user = session['fullname']
    prof = Profile.query.filter_by(userId=id).first()
    job = jobs.query.filter_by(jobTitle=prof.currentJob).limit(9).all()
    if not job:
        job = jobs.query.limit(9).all()
    jobs_list = [j.to_dict() for j in job]
    resp = {
        "jobs": jobs_list,
        "user": user
    }
    return jsonify(resp)

@app.route('/api/profile', methods=['GET'])
def get_user_profile():
    user_id = session['userId']  # Get the user's ID from the session
    user_data = Profile.query.filter_by(userId=user_id).first()  # Replace with function to retrieve user data
    if not user_data:
        return jsonify({"message": "User not found"}), 404
    profile_data = user_data.to_dict()
    return jsonify(profile_data)

@app.route('/api/applicant/<username>',methods=['GET'])
def applicantDetails(username):
    user_data = Profile.query.filter_by(userId=username).first()  # Replace with function to retrieve user data
    if not user_data:
        return jsonify({"message": "User not found"}), 404
    profile_data = user_data.to_dict()
    return jsonify(profile_data)

@app.route('/save-profile', methods=['POST'])
def save_profile():
    data = request.get_json()  # Get the JSON data from the request
    try:      
        userId = session['userId'] 
        name = session['fullname']
        # Convert base64 photo to binary if it's present
        photo_binary = None
        if 'photo' in data:
            import base64
            photo_binary = base64.b64decode(data['photo'])
        # Create a new profile object
        profile = Profile(
            email=data['email'],
            mobile=data['mobile'],
            userId=userId,
            name=name,
            skills="None",
            experience=data['experience'],
            education=data['education'],
            age=data['age'],
            gender=data['gender'],
            aboutMe=data['aboutMe'],
            currentJob=data['currentJob'],
            photo=photo_binary,  # Store the photo as binary data
            hiEd=data['hiEd'],
            portfolio_url=data['portfolio_url'],
            current_company=data['current_company'],
            work_type=data['work_type'],
            start_date=data['start_date'],
            current_location=data['current_location'],
            job_description=data['job_description'],
            recent_jobtitle=data['recent_jobtitle'],
            recent_company=data['recent_company'],
            recent_worktype=data['recent_worktype'],
            recent_duration=data['recent_duration'],
            recent_location=data['recent_location'],
            recent_jobdescription=data['recent_jobdescription'],
            institute=data['institute'],
            duration=data['duration'],
            course_description=data['course_description'],
            skill1=data['skill1'],
            skill2=data.get('skill2'),
            skill3=data.get('skill3'),
            skill4=data.get('skill4'),
            skill5=data.get('skill5')
        )
        # Add profile to the database session
        db.session.add(profile)
        db.session.commit()  # Commit the transaction
        return jsonify({"success": True, "message": "Profile saved successfully!"}), 200
    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify({"success": False, "message": str(e)}), 500

class jobs(db.Model):
    jobId = db.Column(db.Integer, primary_key=True)
    experience = db.Column(db.String)
    qualifications = db.Column(db.String)
    salaryRange = db.Column(db.String)
    location = db.Column(db.String)
    country = db.Column(db.String)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    workType = db.Column(db.String)
    companySize = db.Column(db.String)
    preference = db.Column(db.String)
    contactPerson = db.Column(db.String)
    contact = db.Column(db.String)
    jobTitle = db.Column(db.String)
    role = db.Column(db.String)
    jobPortal = db.Column(db.String)
    jobDescription = db.Column(db.String)
    benefits = db.Column(db.String)
    skills = db.Column(db.String)
    responsibilities = db.Column(db.String)
    companyName = db.Column(db.String)
    companyProfile = db.Column(db.String)
    # If there's a relationship with other models, e.g., applications
    applications = db.relationship('Application', backref='jobs', cascade="all, delete")

    def to_dict(self):
        return {
            "jobId": self.jobId,
            "experience": self.experience,
            "qualifications": self.qualifications,
            "salaryRange": self.salaryRange,
            "location": self.location,
            "country": self.country,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "workType": self.workType,
            "companySize": self.companySize,
            "preference": self.preference,
            "contactPerson": self.contactPerson,
            "contact": self.contact,
            "jobTitle": self.jobTitle,
            "role": self.role,
            "jobPortal": self.jobPortal,
            "jobDescription": self.jobDescription,
            "benefits": self.benefits,
            "skills": self.skills,
            "responsibilities": self.responsibilities,
            "companyName": self.companyName,
            "companyProfile": self.companyProfile
        }

# Users table
class User(db.Model):
    __tablename__ = 'users'
    userId = db.Column(db.Text, primary_key=True)
    fullname = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    is_recruiter = db.Column(db.Boolean, default=False)
    # Relationships
    recruiter = db.relationship('Recruiter', backref='user', uselist=False, cascade="all, delete")
    profile = db.relationship('Profile', backref='user', uselist=False, cascade="all, delete")
    applications = db.relationship('Application', backref='user', cascade="all, delete")
    
# Profile table
class Profile(db.Model):
    __tablename__ = 'Profile'
    
    email = db.Column(db.String)  # Email field
    mobile = db.Column(db.String, primary_key=True)  # Phone number (assuming mobile as primary key here)
    userId = db.Column(db.Text, db.ForeignKey('users.userId'), nullable=False)  # Foreign key referencing 'users'   
    name = db.Column(db.Text, nullable=False)  # Full Name
    resume = db.Column(db.LargeBinary)  # Resume (if uploaded, stored as binary)
    skills = db.Column(db.Text)  # List of skills
    experience = db.Column(db.Text)  # Experience (years or other descriptive data)
    education = db.Column(db.Text)  # Education (e.g. degree, course description)   
    age = db.Column(db.Integer)  # Age
    gender = db.Column(db.String)  # Gender (Male, Female, Other)
    aboutMe = db.Column(db.Text)  # "About Me" Bio section
    currentJob = db.Column(db.String)  # Current job title
    photo = db.Column(db.LargeBinary)  # Profile photo (stored as binary)
    hiEd = db.Column(db.Text)  # Highest Education (degree and course)   
    # Adding fields from your form
    portfolio_url = db.Column(db.String)  # Portfolio URL (if applicable)
    current_company = db.Column(db.String)  # Current company name
    work_type = db.Column(db.String)  # Work type (Full-time, Part-time, Internship)
    start_date = db.Column(db.String)  # Start date of current job
    current_location = db.Column(db.String)  # Location of current job
    job_description = db.Column(db.Text)  # Description of the current job role  
    recent_jobtitle = db.Column(db.String)  # Most recent job title
    recent_company = db.Column(db.String)  # Most recent company
    recent_worktype = db.Column(db.String)  # Recent job's work type
    recent_duration = db.Column(db.String)  # Duration at the recent job
    recent_location = db.Column(db.String)  # Location of the recent job
    recent_jobdescription = db.Column(db.Text)  # Description of the recent job role   
    institute = db.Column(db.String)  # Name of the institute for highest qualification
    duration = db.Column(db.String)  # Duration of the highest education course
    course_description = db.Column(db.Text)  # Course description for highest qualification
    skill1 = db.Column(db.String)  # Skill 1
    skill2 = db.Column(db.String)  # Skill 2
    skill3 = db.Column(db.String)  # Skill 3
    skill4 = db.Column(db.String)  # Skill 4
    skill5 = db.Column(db.String)  # Skill 5

    def to_dict(self):
        photo_base64 = None
        if self.photo:
            photo_base64 = base64.b64encode(self.photo).decode('utf-8')
        return {
            "email": self.email,
            "mobile": self.mobile,
            "userId": self.userId,
            "name": self.name,
            "skills": self.skills,
            "experience": self.experience,
            "education": self.education,
            "age": self.age,
            "gender": self.gender,
            "aboutMe": self.aboutMe,
            "currentJob": self.currentJob,
            "photo": photo_base64,
            "hiEd": self.hiEd,
            "portfolio_url": self.portfolio_url,
            "current_company": self.current_company,
            "work_type": self.work_type,
            "start_date": self.start_date,
            "current_location": self.current_location,
            "job_description": self.job_description,
            "recent_jobtitle": self.recent_jobtitle,
            "recent_company": self.recent_company,
            "recent_worktype": self.recent_worktype,
            "recent_duration": self.recent_duration,
            "recent_location": self.recent_location,
            "recent_jobdescription": self.recent_jobdescription,
            "institute": self.institute,
            "duration": self.duration,
            "course_description": self.course_description,
            "skill1": self.skill1,
            "skill2": self.skill2,
            "skill3": self.skill3,
            "skill4": self.skill4,
            "skill5": self.skill5
        }

# Recruiter table
class Recruiter(db.Model):
    __tablename__ = 'recruiters'
    userId = db.Column(db.Text, db.ForeignKey('users.userId'), primary_key=True)
    company_name = db.Column(db.Text, nullable=False)
    company_description = db.Column(db.Text)
    posts = db.Column(db.Text)
    photo = db.Column(db.LargeBinary)
    url = db.Column(db.String)
    location = db.Column(db.Text)
    size = db.Column(db.Integer)

# Applications table
class Application(db.Model):
    __tablename__ = 'applications'
    applicationId = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Text, db.ForeignKey('users.userId'), nullable=False)
    jobId = db.Column(db.Integer, db.ForeignKey('jobs.jobId'), nullable=False)
    status = db.Column(db.Text)
    portfolio = db.Column(db.String)
    resume = db.Column(db.LargeBinary)

with app.app_context():
    db.create_all()

app.run(debug=True)