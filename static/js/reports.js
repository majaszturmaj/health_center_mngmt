// Funkcja do formatowania daty
function formatReportDate(dateString) {
    const date = new Date(dateString);
    
    // Sprawdź czy data jest poprawna
    if (isNaN(date.getTime())) {
        console.error('Invalid date:', dateString);
        return 'Data niedostępna';
    }
    
    // Formatowanie daty do polskiego formatu
    const day = date.getDate().toString().padStart(2, '0');
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const year = date.getFullYear();
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    
    return `Raport z dnia ${day}.${month}.${year} ${hours}:${minutes}`;
}

// Funkcja do aktualizacji etykiet raportów
function updateReportLabels() {
    const reportElements = document.querySelectorAll('.report-date');
    reportElements.forEach(element => {
        const dateString = element.getAttribute('data-date');
        element.textContent = formatReportDate(dateString);
    });
}

// Funkcja do filtrowania raportów po pacjencie
function filterReportsByPatient(patientId) {
    const reports = document.querySelectorAll('.report-item');
    reports.forEach(report => {
        if (report.getAttribute('data-patient-id') === patientId || !patientId) {
            report.style.display = 'block';
        } else {
            report.style.display = 'none';
        }
    });
}

// Dodaj nasłuchiwanie na kliknięcia w listę pacjentów
function setupPatientListeners() {
    const patientItems = document.querySelectorAll('.patient-item');
    patientItems.forEach(item => {
        item.addEventListener('click', function() {
            // Usuń aktywną klasę ze wszystkich pacjentów
            patientItems.forEach(p => p.classList.remove('active'));
            // Dodaj aktywną klasę do klikniętego pacjenta
            this.classList.add('active');
            // Filtruj raporty dla wybranego pacjenta
            filterReportsByPatient(this.getAttribute('data-patient-id'));
        });
    });
}

// Funkcja inicjalizująca wszystkie funkcjonalności
function initializeReports() {
    updateReportLabels();
    setupPatientListeners();
}

// Wywołaj inicjalizację po załadowaniu strony
document.addEventListener('DOMContentLoaded', initializeReports);
