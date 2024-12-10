from app import db

class jobs(db.Model):
    jobId = db.Column(db.Integer, primary_key=True)
    experience = db.Column(db.String)
    salary = db.Column(db.String)
    qualifications = db.Column(db.String)
    jobDescription = db.Column(db.String)
    skills = db.Column(db.String)
    responsibilities = db.Column(db.String)
    companyName = db.Column(db.String)
    location = db.Column(db.String)
    country = db.Column(db.String)
    workType = db.Column(db.String)
    jobTitle = db.Column(db.String)
    contact = db.Column(db.String)
    role = db.Column(db.String)

    applications = db.relationship('Application', backref='jobs', cascade="all, delete")

    def to_dict(self):
        return {
    "jobId": self.jobId,
    "experience": self.experience,
    "salary": self.salary,
    "qualifications": self.qualifications,
    "jobDescription": self.jobDescription,
    "skills": self.skills,
    "responsibilities": self.responsibilities,
    "companyName": self.companyName,
    "location": self.location,
    "country": self.country,
    "workType": self.workType,
    "jobTitle": self.jobTitle,
    "contact": self.contact,
    "role": self.role
}
class User(db.Model):
    __tablename__ = 'users'
    userId = db.Column(db.Text, primary_key=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    is_recruiter = db.Column(db.Boolean, default=False)

    # Relationships
    recruiter = db.relationship('Recruiter', backref='user', uselist=False, cascade="all, delete")
    profile = db.relationship('Profile', backref='user', uselist=False, cascade="all, delete")
    applications = db.relationship('Application', backref='user', cascade="all, delete")
    chats_sent = db.relationship('Chat', foreign_keys='Chat.sender', backref='sender_user', cascade="all, delete")
    chats_received = db.relationship('Chat', foreign_keys='Chat.recipient', backref='recipient_user', cascade="all, delete")

# Profile table
class Profile(db.Model):
    __tablename__ = 'profile'
    mobile = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Text, db.ForeignKey('users.userId'), nullable=False)
    name = db.Column(db.Text, nullable=False)
    resume = db.Column(db.LargeBinary)
    skills = db.Column(db.Text)
    experience = db.Column(db.Text)
    education = db.Column(db.Text)
    jobs_applied = db.Column(db.Text)

# Recruiter table
class Recruiter(db.Model):
    __tablename__ = 'recruiters'
    userId = db.Column(db.Text, db.ForeignKey('users.userId'), primary_key=True)
    company_name = db.Column(db.Text, nullable=False)
    company_description = db.Column(db.Text)
    posts = db.Column(db.Text)

# Jobs table

# Applications table
class Application(db.Model):
    __tablename__ = 'applications'
    applicationId = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Text, db.ForeignKey('users.userId'), nullable=False)
    jobId = db.Column(db.Integer, db.ForeignKey('jobs.jobId'), nullable=False)
    status = db.Column(db.Text)

# Chats table
class Chat(db.Model):
    __tablename__ = 'chats'
    chatId = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime)
    sender = db.Column(db.Text, db.ForeignKey('users.userId'), nullable=False)
    recipient = db.Column(db.Text, db.ForeignKey('users.userId'), nullable=False)

    # Relationships
    messages = db.relationship('Message', backref='chat', cascade="all, delete")

# Messages table
class Message(db.Model):
    __tablename__ = 'messages'
    messageId = db.Column(db.Integer, primary_key=True)
    chatId = db.Column(db.Integer, db.ForeignKey('chats.chatId'), nullable=False)
    time = db.Column(db.DateTime)
    content = db.Column(db.Text)


