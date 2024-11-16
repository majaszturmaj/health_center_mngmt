### Szybki setup:

1. Run create_database.py
2. Run populate_users.py
3. Run app.py

pip install dotenv

export MAIL_USERNAME='your_email@gmail.com'

export MAIL_PASSWORD='your_password'

# Dokumentacja Systemu Obsługi Pacjentów Szpitala Psychiatrycznego

## Spis treści
1. [Wprowadzenie](#wprowadzenie)
2. [Architektura systemu](#architektura-systemu)
3. [Struktura bazy danych](#struktura-bazy-danych)
4. [Komponenty systemu](#komponenty-systemu)
5. [Funkcjonalności](#funkcjonalności)
6. [Instrukcja uruchomienia](#instrukcja-uruchomienia)
7. [API Endpoints](#api-endpoints)
8. [Bezpieczeństwo](#bezpieczeństwo)

## Wprowadzenie
System służy do zarządzania pacjentami w szpitalu psychiatrycznym, umożliwiając lekarzom i pielęgniarkom prowadzenie dokumentacji medycznej, monitorowanie stanu pacjentów oraz wystawianie e-recept.

![login](https://github.com/user-attachments/assets/749806e8-b0f2-4259-955e-1b2ab8f2770b)

![nurse](https://github.com/user-attachments/assets/d0ea0722-1422-405a-b896-925c58ae632d)

![doctor](https://github.com/user-attachments/assets/3fee05b8-8c43-4991-96fd-4c0df5152a79)


## Architektura systemu
- Framework: Flask (Python)
- Baza danych: MySQL
- Frontend: HTML, JavaScript
- Dodatkowe komponenty: Flask-Mail (obsługa e-recept)

## Struktura bazy danych

![erd](https://github.com/user-attachments/assets/95c15481-f43e-4bbd-a5ab-dc7667203209)



### Tabele:
1. **Users**
   - user_id (PK)
   - username
   - password
   - role
   - created_at

2. **Doctors**
   - doctor_id (PK)
   - user_id (FK)
   - specialization

3. **Patients**
   - patient_id (PK)
   - first_name
   - last_name
   - email
   - date_of_birth
   - gender
   - admission_date
   - assigned_doctor_id (FK)

4. **Reports**
   - report_id (PK)
   - patient_id (FK)
   - nurse_id (FK)
   - report_date
   - mood_level (1-10)
   - anxiety_level (1-10)
   - sleep_quality (good/average/bad)
   - appetite_level (1-10)
   - medication_adherence (boolean)
   - behavioral_observations
   - psychotic_symptoms (boolean)
   - comments

## Komponenty systemu
### Panel Lekarza
- Lista pacjentów
- Historia raportów
- System wystawiania e-recept

### Panel Pielęgniarki
- Lista pacjentów
- Historia raportów
- Formularz nowego raportu
- Edycja/usuwanie raportów

## Funkcjonalności

### Dla Lekarzy
1. Przeglądanie listy pacjentów
2. Dostęp do historii raportów
3. Wystawianie i wysyłanie e-recept
4. Monitorowanie postępów pacjentów

### Dla Pielęgniarek
1. Przeglądanie listy pacjentów
2. Tworzenie raportów dziennych zawierających:
   - Poziom nastroju
   - Poziom lęku
   - Jakość snu
   - Poziom apetytu
   - Przestrzeganie zaleceń dot. leków
   - Objawy psychotyczne
   - Obserwacje behawioralne
3. Edycja i usuwanie raportów

## Instrukcja uruchomienia
1. Utworzenie bazy danych:
   ```bash
   python create_database.py
   ```

2. Populacja użytkowników testowych:
   ```bash
   python populate_users.py
   ```

3. Uruchomienie aplikacji:
   ```bash
   python app.py
   ```

## API Endpoints

### Endpoints dla lekarzy
```
GET /doctor - Panel lekarza
GET /doctor/patients - Lista pacjentów
GET /doctor/reports/<patient_id> - Historia raportów pacjenta
POST /doctor/send_prescription/<patient_id> - Wysłanie e-recepty
```

### Endpoints dla pielęgniarek
```
GET /nurse - Panel pielęgniarki
GET /nurse/patients - Lista pacjentów
GET /nurse/reports/<patient_id> - Historia raportów pacjenta
POST /nurse/add-report - Dodanie nowego raportu
DELETE /nurse/delete_report/<report_id> - Usunięcie raportu
PUT /nurse/reports/<report_id> - Aktualizacja raportu
```

## Bezpieczeństwo
1. Autoryzacja użytkowników poprzez system logowania
2. Rozdzielenie ról (lekarz/pielęgniarka)
3. Zabezpieczenie sesji
4. Szyfrowana komunikacja przy wysyłaniu e-recept (SMTP SSL)
5. Walidacja danych wejściowych
6. Zabezpieczenie przed nieautoryzowanym dostępem do endpointów

---
*Uwaga: System wymaga skonfigurowania zmiennych środowiskowych dla obsługi poczty email (MAIL_USERNAME, MAIL_PASSWORD).*
