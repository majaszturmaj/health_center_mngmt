from database import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'Users'
    __table_args__ = {'extend_existing': True}  # Avoid metadata conflict

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Storing the password directly
    role = db.Column(db.String(20), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)  # Hash the password before storing

    def verify_password(self, password):
        return check_password_hash(self.password, password)  # Verify hashed password

class Doctor(db.Model):
    __tablename__ = 'Doctors'
    doctor_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    specialization = db.Column(db.String(100), nullable=True)

    user = db.relationship('User', backref='doctor')

class Patient(db.Model):
    __tablename__ = 'Patients'
    patient_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    admission_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    assigned_doctor_id = db.Column(db.Integer, db.ForeignKey('Doctors.doctor_id'))

    assigned_doctor = db.relationship('Doctor', backref='Patients')

class Report(db.Model):
    __tablename__ = 'Reports'
    report_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('Patients.patient_id'), nullable=False)
    nurse_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    report_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    mood_level = db.Column(db.Integer)
    anxiety_level = db.Column(db.Integer)
    sleep_quality = db.Column(db.String(10))
    appetite_level = db.Column(db.Integer)
    medication_adherence = db.Column(db.Boolean)
    behavioral_observations = db.Column(db.Text)
    psychotic_symptoms = db.Column(db.Boolean)
    comments = db.Column(db.Text)

    patient = db.relationship('Patient', backref='reports')
    nurse = db.relationship('User', backref='reports')
