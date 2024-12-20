from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from config import Config
from models import User, Patient, Report, Doctor, Instructions
from forms import LoginForm, ReportForm
from flask_login import LoginManager
from database import db, init_db
from datetime import datetime
from flask_mail import Mail, Message
import os
from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user
from dotenv import load_dotenv
load_dotenv()



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  
    db.init_app(app)  

    
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
    patients = Patient.query.all()  
    return jsonify([{'patient_id': p.patient_id, 'name': f"{p.first_name} {p.last_name}"} for p in patients])

@app.route('/doctor/reports/<int:patient_id>')
def get_patient_reports0(patient_id):
    if session.get('role') != 'doctor':
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

@app.route('/doctor/add-report', methods=['POST'])
def add_report_doctor():
    if session.get('role') != 'doctor':
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403

    try:
   
        data = request.form
        new_report = Report(
            patient_id=data['patient_id'],
            nurse_id=session.get('user_id'),
            report_date=datetime.now(),
            mood_level=int(data['mood_level']),
            anxiety_level=int(data['anxiety_level']),
            sleep_quality=data['sleep_quality'],
            appetite_level=int(data['appetite_level']),
            medication_adherence=bool(int(data['medication_adherence'])),
            psychotic_symptoms=bool(int(data['psychotic_symptoms'])),
            behavioral_observations=data.get('behavioral_observations', ''),
            comments=data.get('comments', '')
        )
        db.session.add(new_report)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Raport został pomyślnie dodany'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


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
    patients = Patient.query.all()  
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

@app.route('/nurse/add-report', methods=['POST'])  
def add_report():
    if session.get('role') != 'nurse':
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403

    form = ReportForm()
    
    if form.validate_on_submit():
        try:
            new_report = Report(
                patient_id=request.form.get('patient_id'),  
                nurse_id=session.get('user_id'), 
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

@app.route('/nurse/delete_report/<int:report_id>', methods=['DELETE'])

def delete_report(report_id):
    report = Report.query.get(report_id)
    if report:
        db.session.delete(report)
        db.session.commit()
        return jsonify({"message": "Raport usunięty"}), 200
    else:
        return jsonify({"error": "Raport nie istnieje"}), 404

@app.route('/nurse/reports/<int:report_id>', methods=['PUT'])
def update_report(report_id):
    if session.get('role') != 'nurse':
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    try:
        report = Report.query.get(report_id)
        if not report:
            return jsonify({'success': False, 'error': 'Report not found'}), 404

        data = request.get_json()
        
       
        if 'mood_level' in data:
            report.mood_level = int(data['mood_level'])
        if 'anxiety_level' in data:
            report.anxiety_level = int(data['anxiety_level'])
        if 'sleep_quality' in data:
            report.sleep_quality = data['sleep_quality']
        if 'appetite_level' in data:
            report.appetite_level = int(data['appetite_level'])
        if 'medication_adherence' in data:
            report.medication_adherence = bool(int(data['medication_adherence']))
        if 'psychotic_symptoms' in data:
            report.psychotic_symptoms = bool(int(data['psychotic_symptoms']))
        if 'behavioral_observations' in data:
            report.behavioral_observations = data['behavioral_observations']
        if 'comments' in data:
            report.comments = data['comments']

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Report updated successfully',
            'report': {
                'report_id': report.report_id,
                'report_date': report.report_date.strftime('%Y-%m-%d %H:%M:%S'),
                'mood_level': report.mood_level,
                'anxiety_level': report.anxiety_level,
                'sleep_quality': report.sleep_quality,
                'appetite_level': report.appetite_level,
                'medication_adherence': report.medication_adherence,
                'psychotic_symptoms': report.psychotic_symptoms,
                'behavioral_observations': report.behavioral_observations,
                'comments': report.comments
            }
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')  
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')  
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/doctor/send_prescription/<int:patient_id>', methods=['POST'])
def send_prescription(patient_id):
    data = request.get_json()
    prescription_text = data.get('prescription')
    
    
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({'success': False, 'message': 'Pacjent nie znaleziony'}), 404
    
   
    msg = Message('E-Recepta',
                  sender='your_email@gmail.com',
                  recipients=[patient.email])
    msg.body = f'''
    Pacjent: {patient.first_name} {patient.last_name},
    Dnia: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    Wystawiona e-recepta:

    {prescription_text}

    Pozdrawiam,
    Twój lekarz
    '''
    
    try:
        mail.send(msg)
        return jsonify({'success': True, 'message': 'E-Recepta wysłana pomyślnie'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/doctor/instructions/<int:patient_id>', methods=['GET'])
def get_instructions(patient_id):
    try:
       
        instruction = Instructions.query.filter_by(patient_id=patient_id).order_by(Instructions.created_at.desc()).first()
        
        if instruction:
            return jsonify({
                "instruction_id": instruction.instruction_id,
                "patient_id": instruction.patient_id,
                "doctor_id": instruction.doctor_id,
                "instruction_text": instruction.instruction_text,
                "created_at": instruction.created_at.isoformat()
            })
        else:
            return jsonify([])  
    except Exception as e:
        print(f"Error fetching instructions: {e}")
        return jsonify({"error": "An error occurred while fetching instructions"}), 500


@app.route('/doctor/update-instruction', methods=['POST'])
def update_instruction():
    if session.get('role') != 'doctor':
        return jsonify({"success": False, "message": "Unauthorized access"}), 403
    try:
        data = request.get_json()
        patient_id = data.get('patient_id')
        instruction_text = data.get('instruction_text')
        doctor_id = session.get('user_id')

        if not (patient_id and instruction_text):
            return jsonify({"success": False, "message": "Missing patient ID or instruction text"}), 400

        instruction = Instructions.query.filter_by(patient_id=patient_id).first()
        if instruction:
            instruction.instruction_text = instruction_text
            instruction.doctor_id = doctor_id
            instruction.created_at = datetime.now()
        else:
            instruction = Instructions(
                patient_id=patient_id,
                doctor_id=doctor_id,
                instruction_text=instruction_text,
                created_at=datetime.now()
            )
            db.session.add(instruction)
        db.session.commit()
        return jsonify({'success': True, 'instruction': instruction_text})
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({"success": False, "message": "An error occurred while updating the instruction"}), 500



if __name__ == '__main__':
    app.run(debug=True)
