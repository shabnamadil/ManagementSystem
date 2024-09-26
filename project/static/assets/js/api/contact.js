const CONTACT_URL = `${location.origin}/api/contact/`;
const contactForm = document.getElementById('contactPostForm');
const errorMessagesContainer = document.getElementById('errorMessages');
const succesMessage = document.getElementById('success-message')

async function contact() {
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    const formData = new FormData(contactForm);

    try {
        const response = await fetch(CONTACT_URL, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            },
            body: formData
        });

        if (response.ok) {
            const data = await response.json();
            contactForm.reset();
            console.log('Message was sent successfully.');
            displaySuccessMessage()
        } else {
            const errorData = await response.json();
            displayErrors(errorData);
        }
    } catch (error) {
        console.error('An error occurred:', error);
        displayErrors({ error: 'An unexpected error occurred. Please try again.' });
    }
}

contactForm.addEventListener('submit', function(e) {
    e.preventDefault();
    contact();
});
