from app import create_app
from database import db
from models import Report, Patient, User
from random import randint, choice
from datetime import datetime, timedelta

app = create_app()

with app.app_context():
    # Get all patients and nurses (users with role 'nurse')
    patients = Patient.query.all()
    nurses = User.query.filter_by(role='nurse').all()

    # Define report data for each patient
    reports_data = [
        {
            'patient': 'Wacław Kazimierz',
            'mood_level_range': (3, 6),
            'anxiety_level_range': (7, 10),
            'sleep_quality_options': ['bad', 'average'],
            'appetite_level_range': (3, 6),
            'medication_adherence': True,
            'psychotic_symptoms': True,
            'behavioral_observations': [
                "Pacjent ma silne epizody psychotyczne, wymaga stałej obserwacji.",
                "Pacjent odmawia współpracy, zachowanie niestabilne."
            ],
            'comments': [
                "Wymaga regularnego podawania leków.",
                "Rozmowy z pacjentem są ograniczone ze względu na jego stan."
            ],
            'num_reports': 10
        },
        # Dodaj więcej danych dla innych pacjentów...
    ]

    # Generate reports for each patient over the last 2 weeks
    start_date = datetime.now() - timedelta(weeks=2)

    for data in reports_data:
        # Find the patient by name
        patient = Patient.query.filter_by(first_name=data['patient'].split()[0], last_name=data['patient'].split()[1]).first()
        
    for _ in range(data['num_reports']):
        report_date = start_date + timedelta(days=randint(0, 14))  # Losowo generuj datę raportu
        new_report = Report(
            patient_id=patient.patient_id,
            nurse_id=choice(nurses).user_id,
            report_date=report_date,  # Użyj losowo wygenerowanej daty
            mood_level=randint(*data['mood_level_range']),
            anxiety_level=randint(*data['anxiety_level_range']),
            sleep_quality=choice(data['sleep_quality_options']),
            appetite_level=randint(*data['appetite_level_range']),
            medication_adherence=data['medication_adherence'],
            psychotic_symptoms=data['psychotic_symptoms'],
            behavioral_observations=choice(data['behavioral_observations']),
            comments=choice(data['comments']),  # Dodaj przecinek tutaj
            title=f'Raport z dnia {report_date.strftime("%Y-%m-%d")}'
        )   
        db.session.add(new_report)

    db.session.commit()
    print("Reports have been successfully generated.")
