from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from config import Config
from models import User, Patient, Report, Doctor
from forms import LoginForm, ReportForm
from database import db, init_db
from datetime import datetime

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
            session['user_id'] = user.user_id
            print(f"Logged in as {username} with role {user.role}")
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

@app.route('/nurse/add-report', methods=['POST'])  # Changed from add_report to add-report to match JS
def add_report():
    if session.get('role') != 'nurse':
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403

    form = ReportForm()
    
    if form.validate_on_submit():
        try:
            new_report = Report(
                patient_id=request.form.get('patient_id'),  # You'll need to add this to your form
                nurse_id=session.get('user_id'),  # Make sure you store user_id in session during login
                report_date=datetime.now(),
                mood_level=int(form.mood_level.data),
                anxiety_level=int(form.anxiety_level.data),
                sleep_quality=form.sleep_quality.data,
                appetite_level=int(form.appetite_level.data),
                medication_adherence=bool(int(request.form.get('medication_adherence', 0))),
                psychotic_symptoms=bool(int(request.form.get('psychotic_symptoms', 0))),
                behavioral_observations=form.behavioral_observations.data,
                comments=form.comments.data
            )

            db.session.add(new_report)
            db.session.commit()

            return jsonify({
                'success': True,
                'message': 'Raport dodany pomyślnie',
                'report': {
                    'report_id': new_report.report_id,
                    'report_date': new_report.report_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'mood_level': new_report.mood_level,
                    'anxiety_level': new_report.anxiety_level,
                    'sleep_quality': new_report.sleep_quality,
                    'appetite_level': new_report.appetite_level,
                    'medication_adherence': new_report.medication_adherence,
                    'psychotic_symptoms': new_report.psychotic_symptoms,
                    'behavioral_observations': new_report.behavioral_observations,
                    'comments': new_report.comments
                }
            })

        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500
    
    return jsonify({'success': False, 'error': 'Validation failed', 'errors': form.errors}), 400

if __name__ == '__main__':
    app.run(debug=True)
