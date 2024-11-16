from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from config import Config
from models import User, Patient, Report, Doctor
from forms import LoginForm, ReportForm
from database import db, init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Load configuration from config.py
    db.init_app(app)  # Bind the db instance to the app

    # Ensure the database is initialized
    with app.app_context():
        db.metadata.clear() 
        db.create_all()

    return app

app = create_app()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        print(f"Form submitted: {request.form}")
    if form.validate_on_submit():
        print("Form validated")
        username = form.username.data
        password = form.password.data
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.verify_password(password):
            session['username'] = username
            session['role'] = user.role
            print(f"Logged in as {username} with role {user.role}")  # Debugging info
            return redirect(url_for('doctor_page' if user.role == 'doctor' else 'nurse_page'))
        else:
            flash("Niepoprawne dane logowania", "danger")
    return render_template('login.html', form=form)


@app.route('/doctor')
def doctor_page():
    if 'role' in session and session['role'] == 'doctor':
        return render_template('doctor.html')
    return redirect(url_for('login'))

@app.route('/doctor/patients')
def get_patients0():
    patients = Patient.query.all()  # Assuming you're querying all patients
    return jsonify([{'patient_id': p.patient_id, 'name': f"{p.first_name} {p.last_name}"} for p in patients])

@app.route('/doctor/reports/<int:patient_id>')
def get_patient_reports0(patient_id):
    if session.get('role') != 'doctor':
        return redirect(url_for('login'))

    reports = Report.query.filter_by(patient_id=patient_id).all()
    return jsonify([{
        'report_id': r.report_id,
        'mood_level': r.mood_level,
        'anxiety_level': r.anxiety_level,
        'sleep_quality': r.sleep_quality,
        'appetite_level': r.appetite_level,
        'medication_adherence': r.medication_adherence,
        'psychotic_symptoms': r.psychotic_symptoms,
        'behavioral_observations': r.behavioral_observations,
        'comments': r.comments
    } for r in reports])

@app.route('/nurse')
def nurse_page():
    role = session.get('role')
    if role == 'nurse':
        patients = Patient.query.all()
        reports = Report.query.order_by(Report.report_date.desc()).all()
        form = ReportForm() 
        return render_template('nurse.html',
                                patients=patients, 
                                reports=reports,
                                form=form)
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/nurse/patients')
def get_patients1():
    patients = Patient.query.all()  # Assuming you're querying all patients
    return jsonify([{'patient_id': p.patient_id, 'name': f"{p.first_name} {p.last_name}"} for p in patients])


@app.route('/nurse/reports/<int:patient_id>')
def get_patient_reports1(patient_id):
    if session.get('role') != 'nurse':
        return redirect(url_for('login'))

    reports = Report.query.filter_by(patient_id=patient_id).all()
    return jsonify([{
    	'report_date' : r.report_date,
        'report_id': r.report_id,
        'mood_level': r.mood_level,
        'anxiety_level': r.anxiety_level,
        'sleep_quality': r.sleep_quality,
        'appetite_level': r.appetite_level,
        'medication_adherence': r.medication_adherence,
        'psychotic_symptoms': r.psychotic_symptoms,
        'behavioral_observations': r.behavioral_observations,
        'comments': r.comments
    } for r in reports])

@app.route('/nurse/add_report', methods=['POST'])
def add_report():
    if session.get('role') != 'nurse':
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403

    data = request.get_json()  # Retrieve JSON data from the request
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400

    # Validate required fields
    required_fields = [
        'patient_id', 'mood_level', 'anxiety_level', 'sleep_quality', 
        'appetite_level', 'medication_adherence', 'psychotic_symptoms'
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({'success': False, 'error': f'Missing field: {field}'}), 400

    # Check data types and constraints
    try:
        patient_id = int(data['patient_id'])
        mood_level = int(data['mood_level'])
        anxiety_level = int(data['anxiety_level'])
        appetite_level = int(data['appetite_level'])
        sleep_quality = data['sleep_quality']
        medication_adherence = bool(data['medication_adherence'])
        psychotic_symptoms = bool(data['psychotic_symptoms'])

        # Validate ranges
        if not (1 <= mood_level <= 10):
            return jsonify({'success': False, 'error': 'Mood level must be between 1 and 10'}), 400
        if not (1 <= anxiety_level <= 10):
            return jsonify({'success': False, 'error': 'Anxiety level must be between 1 and 10'}), 400
        if not (1 <= appetite_level <= 10):
            return jsonify({'success': False, 'error': 'Appetite level must be between 1 and 10'}), 400
        if sleep_quality not in ['good', 'average', 'bad']:
            return jsonify({'success': False, 'error': 'Sleep quality must be one of: good, average, bad'}), 400

        # Create new report instance
        new_report = Report(
            patient_id=patient_id,
            nurse_id=session['user_id'],
            mood_level=mood_level,
            anxiety_level=anxiety_level,
            sleep_quality=sleep_quality,
            appetite_level=appetite_level,
            medication_adherence=medication_adherence,
            psychotic_symptoms=psychotic_symptoms,
            behavioral_observations=data.get('behavioral_observations', ''),
            comments=data.get('comments', '')
        )

        db.session.add(new_report)
        db.session.commit()

        # Respond with success and data about the newly added report
        return jsonify({'success': True, 'report': {
            'mood_level': new_report.mood_level,
            'anxiety_level': new_report.anxiety_level,
            'sleep_quality': new_report.sleep_quality,
            'appetite_level': new_report.appetite_level,
            'medication_adherence': new_report.medication_adherence,
            'psychotic_symptoms': new_report.psychotic_symptoms,
            'behavioral_observations': new_report.behavioral_observations,
            'comments': new_report.comments
        }})

    except (ValueError, TypeError) as e:
        return jsonify({'success': False, 'error': f'Invalid data: {str(e)}'}), 400

    # If validation fails for any reason, return this response
    return jsonify({'success': False, 'error': 'Validation failed'}), 400

if __name__ == '__main__':
    app.run(debug=True)
