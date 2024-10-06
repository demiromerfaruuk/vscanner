document.addEventListener('DOMContentLoaded', function() {
    var socket = io();
    socket.on('connect', function() {
        console.log('Connected to server');
    });
    socket.on('scan_progress', function(data) {
        console.log('Progress:', data.progress);
        var progressElement = document.getElementById('progress');
        progressElement.style.height = data.progress + '%';
        document.getElementById('progress-text').innerText = data.progress + '%';
    });
    socket.on('scan_complete', function(data) {
        console.log('Scan complete event received:', data);
        alert('Tarama tamamlandı. Sonuçlar sayfasına yönlendiriliyorsunuz.');
        var form = document.createElement('form');
        form.method = 'POST';
        form.action = '/scan_results';
        
        var alertsInput = document.createElement('input');
        alertsInput.type = 'hidden';
        alertsInput.name = 'alerts';
        alertsInput.value = data.alerts;
        form.appendChild(alertsInput);
        
        var pdfInput = document.createElement('input');
        pdfInput.type = 'hidden';
        pdfInput.name = 'pdf_filename';
        pdfInput.value = data.pdf_filename;
        form.appendChild(pdfInput);
        
        document.body.appendChild(form);
        form.submit();
    });
    socket.on('scan_error', function(data) {
        console.error('Scan error:', data.error);
        alert('Tarama sırasında bir hata oluştu: ' + data.error);
    });
    socket.on('disconnect', function() {
        console.log('Disconnected from server');
    });
});