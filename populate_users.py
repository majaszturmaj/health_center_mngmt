from app import create_app  # Import the create_app function
from database import db  # Import your database instance
from models import User  # Import your User model
from sqlalchemy import text  # Import the text function for raw SQL

app = create_app()  # Create your Flask app

with app.app_context():  # Create application context
    # Clear the Patients table first
    db.session.execute(text('DELETE FROM Patients;'))  # Delete all patients
    db.session.commit()  # Commit the delete operation

    # Next, clear the Doctors table
    db.session.execute(text('DELETE FROM Doctors;'))  # Delete all doctors
    db.session.commit()  # Commit the delete operation

    # Finally, clear the Users table
    db.session.execute(text('DELETE FROM Users;'))  # Delete all users
    db.session.commit()  # Commit the delete operation

    # Example users
    users = [
        {'username': 'nurse1', 'password': 'nurse_password', 'role': 'nurse'},
        {'username': 'doctor1', 'password': 'doctor_password1', 'role': 'doctor'},
        {'username': 'doctor2', 'password': 'doctor_password2', 'role': 'doctor'}
    ]

    for user_data in users:
        user = User(username=user_data['username'], role=user_data['role'])
        user.set_password(user_data['password'])  # Hash the password
        db.session.add(user)  # Add user to the session

    db.session.commit()  # Commit all changes to the database
    print("Users added with hashed passwords.")
