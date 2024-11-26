
function formatReportDate(dateString) {
    const date = new Date(dateString);
    

    if (isNaN(date.getTime())) {
        console.error('Invalid date:', dateString);
        return 'Data niedostępna';
    }
    
  
    const day = date.getDate().toString().padStart(2, '0');
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const year = date.getFullYear();
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    
    return `Raport z dnia ${day}.${month}.${year} ${hours}:${minutes}`;
}


function updateReportLabels() {
    const reportElements = document.querySelectorAll('.report-date');
    reportElements.forEach(element => {
        const dateString = element.getAttribute('data-date');
        element.textContent = formatReportDate(dateString);
    });
}


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


function setupPatientListeners() {
    const patientItems = document.querySelectorAll('.patient-item');
    patientItems.forEach(item => {
        item.addEventListener('click', function() {
      
            patientItems.forEach(p => p.classList.remove('active'));
           
            this.classList.add('active');
           
            filterReportsByPatient(this.getAttribute('data-patient-id'));
        });
    });
}


function initializeReports() {
    updateReportLabels();
    setupPatientListeners();
}


document.addEventListener('DOMContentLoaded', initializeReports);
