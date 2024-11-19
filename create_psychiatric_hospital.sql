-- Drop the database if it exists
DROP DATABASE IF EXISTS psychiatric_hospital;

-- Create the database
CREATE DATABASE psychiatric_hospital;
USE psychiatric_hospital;

-- Table Users
CREATE TABLE IF NOT EXISTS Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,  -- Role of the user (nurse, doctor)
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table Doctors
CREATE TABLE IF NOT EXISTS Doctors (
    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    specialization VARCHAR(100),  -- Doctor's specialization
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE  -- Cascade delete
);


-- Table Patients
CREATE TABLE IF NOT EXISTS Patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    date_of_birth DATE NOT NULL,
    gender ENUM('male', 'female', 'other') NOT NULL,  -- Patient's gender
    admission_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    assigned_doctor_id INT,
    FOREIGN KEY (assigned_doctor_id) REFERENCES Doctors(doctor_id)  -- Foreign key to doctors
);

-- Table Reports
CREATE TABLE IF NOT EXISTS Reports (
    report_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    nurse_id INT NOT NULL,
    report_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    mood_level INT CHECK (mood_level BETWEEN 1 AND 10),  -- Patient's mood level (1-10)
    anxiety_level INT CHECK (anxiety_level BETWEEN 1 AND 10),  -- Patient's anxiety level (1-10)
    sleep_quality ENUM('good', 'average', 'bad') NOT NULL,  -- Sleep quality
    appetite_level INT CHECK (appetite_level BETWEEN 1 AND 10),  -- Patient's appetite level (1-10)
    medication_adherence BOOLEAN NOT NULL,  -- Treatment adherence
    behavioral_observations TEXT,  -- Behavioral observations
    psychotic_symptoms BOOLEAN NOT NULL,  -- Psychotic symptoms
    comments TEXT,  -- Additional comments about the patient
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),  -- Foreign key to patients
    FOREIGN KEY (nurse_id) REFERENCES Users(user_id)  -- Foreign key to users
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


