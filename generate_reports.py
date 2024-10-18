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

    # Generate reports for each patient
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
        {
            'patient': 'Emilia Walewska',
            'mood_level_range': (8, 10),
            'anxiety_level_range': (1, 3),
            'sleep_quality_options': ['good'],
            'appetite_level_range': (8, 10),
            'medication_adherence': True,
            'psychotic_symptoms': False,
            'behavioral_observations': ["Pacjentka w dobrym stanie, bez widocznych objawów zaburzeń."],
            'comments': ["Rutynowa kontrola, brak nieprawidłowości."],
            'num_reports': 7
        },
        {
            'patient': 'Alicja Kopytko',
            'mood_level_range': (1, 4),
            'anxiety_level_range': (7, 10),
            'sleep_quality_options': ['bad', 'average'],
            'appetite_level_range': (2, 4),
            'medication_adherence': True,
            'psychotic_symptoms': False,
            'behavioral_observations': [
                "Pacjentka w głębokiej depresji, wymaga wsparcia psychologicznego.",
                "Zachowania apatyczne, brak motywacji do współpracy."
            ],
            'comments': ["Przedłużona hospitalizacja z uwagi na stan psychiczny."],
            'num_reports': 12
        },
        {
            'patient': 'Ziemowit Twaróg',
            'mood_level_range': (4, 6),
            'anxiety_level_range': (5, 7),
            'sleep_quality_options': ['average'],
            'appetite_level_range': (4, 6),
            'medication_adherence': False,
            'psychotic_symptoms': False,
            'behavioral_observations': [
                "Pacjent planuje ucieczkę, przejawia zwiększoną czujność.",
                "Odmowa przyjmowania leków, próby manipulacji personelem."
            ],
            'comments': ["Wymaga wzmożonego nadzoru."],
            'num_reports': 10
        },
        {
            'patient': 'Jude Twaróg',
            'mood_level_range': (6, 8),
            'anxiety_level_range': (4, 6),
            'sleep_quality_options': ['average', 'bad'],
            'appetite_level_range': (5, 7),
            'medication_adherence': True,
            'psychotic_symptoms': False,
            'behavioral_observations': [
                "Pacjent ma epizody manii, rozmawia chaotycznie i energicznie.",
                "Nadmierna aktywność, trudności z koncentracją."
            ],
            'comments': ["Rodzic Ziemowita, wykazuje chęć wsparcia, ale jest emocjonalnie niestabilny."],
            'num_reports': 10
        }
    ]

    # Generate reports for each patient over 2 weeks
    start_date = datetime.now() - timedelta(weeks=2)

    for data in reports_data:
        patient = Patient.query.filter_by(first_name=data['patient'].split()[0], last_name=data['patient'].split()[1]).first()
        
        for _ in range(data['num_reports']):
            report_date = start_date + timedelta(days=randint(0, 14))
            new_report = Report(
                patient_id=patient.patient_id,
                nurse_id=choice(nurses).user_id,
                report_date=report_date,
                mood_level=randint(*data['mood_level_range']),
                anxiety_level=randint(*data['anxiety_level_range']),
                sleep_quality=choice(data['sleep_quality_options']),
                appetite_level=randint(*data['appetite_level_range']),
                medication_adherence=data['medication_adherence'],
                psychotic_symptoms=data['psychotic_symptoms'],
                behavioral_observations=choice(data['behavioral_observations']),
                comments=choice(data['comments'])
            )
            db.session.add(new_report)

    db.session.commit()

    print("Reports have been successfully generated.")