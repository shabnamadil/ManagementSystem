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
            // Handle success (e.g., redirect to a success page or show a message)
            sessionStorage.setItem('email', data.email);
            window.location.href = '/dashboard/verify/';
            console.log('Registration successful:', data);
        } else {
            const errorData = await response.json();
            // Handle error (e.g., display error messages)
            console.log('Registration failed:', errorData);
        }
    } catch (error) {
        console.error('An error occurred:', error);
    }
}

registerForm.addEventListener('submit', function(e) {
    e.preventDefault();
    register();
    registerForm.reset()
});
