const LOGIN_URL = `${location.origin}/api/token/`;
const loginForm = document.getElementById('loginForm');

async function login() {
    const formData = new FormData(loginForm);

    const formObject = {};
    formData.forEach((value, key) => formObject[key] = value);

    try {
        const response = await fetch(LOGIN_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formObject)
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('token', data.access);
            window.location.href = `${location.origin}`
            console.log('Login successful');
        } else {
            const errorData = await response.json();
            console.log('Login failed:', errorData);
        }
    } catch (error) {
        console.error('An error occurred:', error);
    }
}

loginForm.addEventListener('submit', function(e) {
    e.preventDefault();
    login();
    loginForm.reset();
});
