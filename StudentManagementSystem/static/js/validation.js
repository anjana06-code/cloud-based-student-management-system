/* 
  Form Validation JavaScript
*/

function validateEmail(email) {
    const re = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return re.test(String(email).toLowerCase());
}

function validateRegisterForm() {
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm_password').value;

    if (name.length < 2) {
        alert('Please enter your full name (at least 2 characters).');
        return false;
    }

    if (!validateEmail(email)) {
        alert('Please enter a valid email address.');
        return false;
    }

    if (password.length < 6) {
        alert('Password must be at least 6 characters long.');
        return false;
    }

    if (password !== confirmPassword) {
        alert('Passwords do not match. Please verify your password.');
        return false;
    }

    return true;
}

function validateFileUpload() {
    const fileInput = document.getElementById('assignment_file');
    if (!fileInput || fileInput.files.length === 0) {
        alert('Please select a file to upload.');
        return false;
    }

    const file = fileInput.files[0];
    const allowedExtensions = ['pdf', 'doc', 'docx', 'zip', 'txt', 'png', 'jpg', 'jpeg'];
    const fileExt = file.name.split('.').pop().toLowerCase();

    if (!allowedExtensions.includes(fileExt)) {
        alert('Invalid file format. Allowed formats: ' + allowedExtensions.join(', '));
        return false;
    }

    // Limit size to 10MB
    const maxSizeInBytes = 10 * 1024 * 1024;
    if (file.size > maxSizeInBytes) {
        alert('File size exceeds 10 MB limit.');
        return false;
    }

    return true;
}
