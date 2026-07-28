/* 
  Global Interactive UI JavaScript
*/

document.addEventListener('DOMContentLoaded', function() {
    console.log('Student Management System script initialized.');

    // 1. Auto-dismiss alert notifications after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(function() {
                if (alert.parentNode) {
                    alert.parentNode.removeChild(alert);
                }
            }, 500);
        }, 5000);
    });

    // 2. Alert manual close button
    const closeBtns = document.querySelectorAll('.alert-close');
    closeBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            const alert = this.closest('.alert');
            if (alert) {
                alert.remove();
            }
        });
    });

    // 3. Confirm Delete Prompts
    const deleteForms = document.querySelectorAll('.form-delete-confirm');
    deleteForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const message = form.getAttribute('data-confirm-message') || 'Are you sure you want to delete this record?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // 4. File input filename display on select
    const fileInput = document.getElementById('assignment_file');
    const fileNameDisplay = document.getElementById('file_name_display');
    if (fileInput && fileNameDisplay) {
        fileInput.addEventListener('change', function() {
            if (fileInput.files.length > 0) {
                fileNameDisplay.textContent = 'Selected file: ' + fileInput.files[0].name;
                fileNameDisplay.style.color = '#1e3a8a';
                fileNameDisplay.style.fontWeight = 'bold';
            } else {
                fileNameDisplay.textContent = 'No file selected';
            }
        });
    }
});
