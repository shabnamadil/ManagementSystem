const BASE_URL = `${location.origin}/api/register/`;
const registerForm = document.getElementById('registerForm');


async function register() {
    const formData = new FormData(registerForm);
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    try {
        const response = await fetch(BASE_URL, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            },
            body: formData
        });
        
        if (response.ok) {
            const data = await response.json();
            registerForm.reset();
            localStorage.setItem('email', data.email);
            localStorage.setItem('registrationSuccess', 'true');
            displaySuccessMessage();
    
            setTimeout(() => {
                window.location.href = '/dashboard/verify/';
            }, 10000);

        } else {
            const errorData = await response.json();
            displayErrors(errorData);
        }
    } catch (error) {
        console.error('An error occurred:', error);
    }
}

registerForm.addEventListener('submit', function(e) {
    e.preventDefault();
    register();
});
