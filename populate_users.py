from app import create_app  # Import the create_app function
from database import db  # Import your database instance
from models import User, Doctor, Patient  # Import your models
from sqlalchemy import text  # Import the text function for raw SQL

app = create_app()  # Create your Flask app

with app.app_context():  # Create application context
    # Clear the tables in the correct order to respect foreign key constraints
    db.session.execute(text('DELETE FROM Patients;'))
    db.session.execute(text('DELETE FROM Doctors;'))
    db.session.execute(text('DELETE FROM Users;'))
    db.session.commit()

    # Add example users (nurses and doctors)
    users = [
        {'username': 'nurse1', 'password': 'nurse_password', 'role': 'nurse'},
        {'username': 'doctor1', 'password': 'doctor_password1', 'role': 'doctor'},
        {'username': 'doctor2', 'password': 'doctor_password2', 'role': 'doctor'}
    ]

    user_objects = []
    for user_data in users:
        user = User(username=user_data['username'], role=user_data['role'])
        user.set_password(user_data['password'])  # Hash the password
        user_objects.append(user)
        db.session.add(user)

    db.session.commit()  # Commit the users first, so they have user_ids

    # Add doctors using the user_id from the previously created users
    doctors = [
        {'user_id': user_objects[1].user_id, 'specialization': 'Psychiatry'},
        {'user_id': user_objects[2].user_id, 'specialization': 'Clinical Psychology'}
    ]

    doctor_objects = []
    for doctor_data in doctors:
        doctor = Doctor(user_id=doctor_data['user_id'], specialization=doctor_data['specialization'])
        doctor_objects.append(doctor)
        db.session.add(doctor)

    db.session.commit()  # Commit doctors, now we can retrieve their doctor_ids

    # Add example patients assigned to the correct doctors by doctor_id
    patients = [
        {'first_name': 'John', 'last_name': 'Doe', 'date_of_birth': '1990-01-01', 'gender': 'male', 'assigned_doctor_id': doctor_objects[0].doctor_id},
        {'first_name': 'Jane', 'last_name': 'Smith', 'date_of_birth': '1985-05-15', 'gender': 'female', 'assigned_doctor_id': doctor_objects[1].doctor_id},
        {'first_name': 'Alice', 'last_name': 'Johnson', 'date_of_birth': '2000-08-20', 'gender': 'female', 'assigned_doctor_id': doctor_objects[0].doctor_id},
        {'first_name': 'Bob', 'last_name': 'Brown', 'date_of_birth': '1975-11-30', 'gender': 'male', 'assigned_doctor_id': doctor_objects[1].doctor_id},
        {'first_name': 'Charlie', 'last_name': 'Davis', 'date_of_birth': '1995-02-10', 'gender': 'other', 'assigned_doctor_id': doctor_objects[0].doctor_id}
    ]

    for patient_data in patients:
        patient = Patient(
            first_name=patient_data['first_name'],
            last_name=patient_data['last_name'],
            date_of_birth=patient_data['date_of_birth'],
            gender=patient_data['gender'],
            assigned_doctor_id=patient_data['assigned_doctor_id']
        )
        db.session.add(patient)

    db.session.commit()  # Commit patients

    print("Users, doctors, and patients have been successfully added.")
