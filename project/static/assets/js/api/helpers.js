function translateMessage(message) {
    const translations = {
        "This field may not be blank.": "Bu sahə tələb edilir.",
    };

    return translations[message] || message;
}

function handleFocus(field, messageList, messages) {
    if (field) {
        field.classList.add('border', 'border-red-400');
        const errorElement = field.nextElementSibling;

        if (errorElement && errorElement.classList.contains('error-message')) {
            errorElement.textContent = messageList; 
            errorElement.classList.remove('hidden');
        }

        field.addEventListener('input', function() {
            if (messages.length === 0) return; 
            field.classList.remove('border', 'border-red-400');
            if (errorElement) {
                errorElement.textContent = '';
                errorElement.classList.add('hidden');
            }
        });
    }
}

function displayErrors(errors) {
    for (const [fieldName, messages] of Object.entries(errors)) {
        const translatedMessages = messages.map(message => translateMessage(message));
        const messageList = translatedMessages.join(' ');
        const field = document.querySelector(`[name="${fieldName}"]`);
        handleFocus(field, messageList, messages)
    }
}

function displaySuccessMessage() {
    const successMessage = document.getElementById('successMessage');
    successMessage.classList.remove('hidden');

    setTimeout(() => {
        successMessage.classList.add('hidden'); 
    }, 10000); // 10 seconds
}

function closeSuccessMessage() {
    const successMessage = document.getElementById('successMessage');
    successMessage.classList.add('hidden');
}