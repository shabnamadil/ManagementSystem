const BASE_URL = `${location.origin}/api/verify-otp/`;
const verifyRegisterForm = document.getElementById('verifyRegisterForm');


async function verify() {
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    const formData = new FormData(verifyRegisterForm);
    formData.append('email', localStorage.getItem('email'))
    
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
            console.log('Verified successfully:', data);
            localStorage.removeItem('email')
        } else {
            const errorData = await response.json();
            // Handle error (e.g., display error messages)
            console.log('Verification failed:', errorData);
        }
    } catch (error) {
        console.error('An error occurred:', error);
    }
}

verifyRegisterForm.addEventListener('submit', function(e) {
    e.preventDefault();
    verify();
});
