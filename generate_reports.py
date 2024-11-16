from app import create_app
from database import db
from models import Report, Patient, User
from random import randint, choice
from datetime import datetime, timedelta

app = create_app()

with app.app_context():
    # Get all patients and nurses
    patients = Patient.query.all()
    nurses = User.query.filter_by(role='nurse').all()
    
    # Define common report options that będą używane dla wszystkich pacjentów
    common_options = {
        'sleep_quality_options': ['good', 'average', 'bad'],
        'behavioral_observations': [
            "Pacjent współpracuje podczas terapii",
            "Pacjent wykazuje oznaki poprawy",
            "Pacjent wymaga dodatkowej uwagi",
            "Pacjent ma trudności ze snem",
            "Pacjent zgłasza problemy z apetytem"
        ],
        'comments': [
            "Kontynuacja obecnego planu leczenia",
            "Rozważyć modyfikację dawki leków",
            "Zalecana konsultacja z psychologiem",
            "Wymaga częstszych obserwacji",
            "Postępy w terapii są zadowalające"
        ]
    }

    # Generate reports for all patients
    start_date = datetime.now() - timedelta(weeks=2)
    
    for patient in patients:
        # Generate between 5 and 10 reports for each patient
        num_reports = randint(5, 10)
        
        for _ in range(num_reports):
            # Generate random date within last 2 weeks
            report_date = start_date + timedelta(days=randint(0, 14), 
                                               hours=randint(0, 23), 
                                               minutes=randint(0, 59))
            
            # Create new report with randomized but realistic data
            new_report = Report(
                patient_id=patient.patient_id,
                nurse_id=choice(nurses).user_id,
                report_date=report_date,
                mood_level=randint(1, 10),
                anxiety_level=randint(1, 10),
                sleep_quality=choice(common_options['sleep_quality_options']),
                appetite_level=randint(1, 10),
                medication_adherence=choice([True, True, False]),  # 2/3 chance of adherence
                psychotic_symptoms=choice([True, False, False, False]),  # 1/4 chance of symptoms
                behavioral_observations=choice(common_options['behavioral_observations']),
                comments=choice(common_options['comments'])
            )
            
            db.session.add(new_report)
    
    db.session.commit()
    print("Reports have been successfully generated for all patients.")
