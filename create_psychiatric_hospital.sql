
DROP DATABASE IF EXISTS psychiatric_hospital;


CREATE DATABASE psychiatric_hospital;
USE psychiatric_hospital;

-- Table Users
CREATE TABLE IF NOT EXISTS Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,  
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table Doctors
CREATE TABLE IF NOT EXISTS Doctors (
    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    specialization VARCHAR(100),  
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE  
);


-- Table Patients
CREATE TABLE IF NOT EXISTS Patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    date_of_birth DATE NOT NULL,
    gender ENUM('male', 'female', 'other') NOT NULL,  
    admission_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    assigned_doctor_id INT,
    FOREIGN KEY (assigned_doctor_id) REFERENCES Doctors(doctor_id)  
);

-- Table Reports
CREATE TABLE IF NOT EXISTS Reports (
    report_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    nurse_id INT NOT NULL,
    report_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    mood_level INT CHECK (mood_level BETWEEN 1 AND 10), 
    anxiety_level INT CHECK (anxiety_level BETWEEN 1 AND 10),  
    sleep_quality ENUM('good', 'average', 'bad') NOT NULL,  
    appetite_level INT CHECK (appetite_level BETWEEN 1 AND 10),  
    medication_adherence BOOLEAN NOT NULL,  
    behavioral_observations TEXT,  
    psychotic_symptoms BOOLEAN NOT NULL,  
    comments TEXT, 
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),  
    FOREIGN KEY (nurse_id) REFERENCES Users(user_id)  
);

-- Instructions
CREATE TABLE IF NOT EXISTS Instructions (
    instruction_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    instruction_text TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id)
);


