const RESEND_OTP_URL = `${location.origin}/api/resend-otp/`;
const resendButton = document.getElementById('resendVerifyCode');

async function resendOtp() {
    const email = localStorage.getItem('email'); // Retrieve email without additional argument
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    try {
        const response = await fetch(RESEND_OTP_URL, { // Use the correct URL
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ email }) // Wrap the email in an object
        });
        
        if (response.ok) {
            const data = await response.json();
            // Handle success (e.g., redirect to a success page or show a message)
            console.log('OTP was sent successfully:', data);
            sessionStorage.removeItem('email');
        } else {
            const errorData = await response.json();
            // Handle error (e.g., display error messages)
            console.log('OTP sending failed:', errorData);
        }
    } catch (error) {
        console.error('An error occurred:', error);
    }
}

resendButton.addEventListener('click', function(e) {
    e.preventDefault();
    resendOtp();
});
