from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import Config
from models import User, Patient, Report, Doctor
from forms import LoginForm
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

@app.route('/nurse')
def nurse_page():
    role = session.get('role')  # Debugging
    print(f"Current session role: {role}")  # Check role
    if role == 'nurse':
        return render_template('nurse.html')
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
