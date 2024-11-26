from app import create_app  
from database import db  
from models import User, Doctor, Patient  
from sqlalchemy import text  

app = create_app()  

with app.app_context():  
    
    db.session.execute(text('DELETE FROM Patients;'))
    db.session.execute(text('DELETE FROM Doctors;'))
    db.session.execute(text('DELETE FROM Users;'))
    db.session.commit()

    
    users = [
        {'username': 'nurse1', 'password': 'nurse_password', 'role': 'nurse'},
        {'username': 'doctor1', 'password': 'doctor_password1', 'role': 'doctor'},
        {'username': 'doctor2', 'password': 'doctor_password2', 'role': 'doctor'}
    ]

    user_objects = []
    for user_data in users:
        user = User(username=user_data['username'], role=user_data['role'])
        user.set_password(user_data['password']) 
        user_objects.append(user)
        db.session.add(user)

    db.session.commit()  

    doctors = [
        {'user_id': user_objects[1].user_id, 'specialization': 'Psychiatry'},
        {'user_id': user_objects[2].user_id, 'specialization': 'Clinical Psychology'}
    ]

    doctor_objects = []
    for doctor_data in doctors:
        doctor = Doctor(user_id=doctor_data['user_id'], specialization=doctor_data['specialization'])
        doctor_objects.append(doctor)
        db.session.add(doctor)

    db.session.commit()  

   
    patients = [
        {'first_name': 'Wacław', 'last_name': 'Kazimierz', 'email':'kawac@kawoc.com', 'date_of_birth': '1990-01-01', 'gender': 'male', 'assigned_doctor_id': doctor_objects[0].doctor_id},
        {'first_name': 'Emilia', 'last_name': 'Walewska', 'email':'kmrkfen@jkekvfk.erfee', 'date_of_birth': '1985-05-15', 'gender': 'female', 'assigned_doctor_id': doctor_objects[1].doctor_id},
        {'first_name': 'Alicja', 'last_name': 'Kopytko', 'email':'kmrkfen@jkekvfk2.erfee','date_of_birth': '2000-08-20', 'gender': 'female', 'assigned_doctor_id': doctor_objects[0].doctor_id},
        {'first_name': 'Ziemowit', 'last_name': 'Twaróg', 'email':'kmrkfen@jkekvfk3.erfee','date_of_birth': '1975-11-30', 'gender': 'male', 'assigned_doctor_id': doctor_objects[1].doctor_id},
        {'first_name': 'Jude', 'last_name': 'Twaróg','email':'maja.szturmaj@gmail.com', 'date_of_birth': '1995-02-10', 'gender': 'other', 'assigned_doctor_id': doctor_objects[0].doctor_id}
    ]

    for patient_data in patients:
        patient = Patient(
            first_name=patient_data['first_name'],
            last_name=patient_data['last_name'],
            email=patient_data['email'],
            date_of_birth=patient_data['date_of_birth'],
            gender=patient_data['gender'],
            assigned_doctor_id=patient_data['assigned_doctor_id']
        )
        db.session.add(patient)

    db.session.commit()  

    print("Users, doctors, and patients have been successfully added.")
    import generate_reports  
