var selectedUsersArray = [];
var selectedCategoriesArray = [];

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function createWorkspace() {
    var form = document.getElementById('createWorkspaceForm');
    var formData = new FormData(form);
    // var imageInput = document.getElementById('workspace-image');
    // Create an empty object to store key-value pairs
    var formDataObject = {};

    // Iterate over the FormData entries and add them to the object
    formData.forEach(function(value, key) {
        formDataObject[key] = value;
    });
    // Convert the selectedUsersArray and selectedCategoriesArray to JSON and add them to the object
    formDataObject['users'] = selectedUsersArray;
    formDataObject['categories'] = selectedCategoriesArray;
    // Now formDataObject contains all form data and additional arrays as JSON
    var formDataJSON = JSON.stringify(formDataObject);

    // You can use formDataJSON as needed
    fetch('/create-workspace/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: formDataJSON
    })
    .then(response => {
        // Check if the response status is Created (201)
        if (response.status === 201) {
            console.log('Workspace created successfully!');
                setTimeout(function(){
                window.location.href = '/workspaces/';
            }, 50);
        } else {
            console.error('Unexpected response status:', response.status);
            console.error('Unexpected response status:', response.status);
        }
    })
    .catch(error => {
        console.error('Error during fetch operation:', error);
    });
}




function searchUsers() {
    var input, filter, userList, options, option, i, txtValue, found = false;
    input = document.getElementById('searchInput');
    filter = input.value.toUpperCase();
    userList = document.getElementById('userList');
    options = userList.getElementsByTagName('option');

    for (i = 0; i < options.length; i++) {
        option = options[i];
        txtValue = option.textContent || option.innerText;

        if (!found && txtValue.toUpperCase().indexOf(filter) > -1) {
            // If not found yet, make the option the selected option
            userList.selectedIndex = i;
            found = true;
        }

        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            option.style.display = "";
        } else {
            option.style.display = "none";
        }
    }
}

function addUser() {
    var selectedUsersDiv = document.getElementById('selectedUsers');
    var userList = document.getElementById('userList');
    var selectedOption = userList.options[userList.selectedIndex];
    if (selectedOption) {
        var userName = selectedOption.text;
        var userID = Number(selectedOption.value);

        // Check if the user is already selected
        if (!selectedUsersArray.includes(userID)) {
            // Add the user to the array
            selectedUsersArray.push(userID);

            // Update the FormData
            updateFormData();

            var card = document.createElement('div');
            card.className = 'card mb-2 mr-2';

            var cardBody = document.createElement('div');
            cardBody.className = 'card-body d-flex flex-row align-items-center';

            var userNameText = document.createTextNode(userName);
            cardBody.appendChild(userNameText);

            var removeButton = document.createElement('button');
            removeButton.className = 'border-0 bg-transparent';
            removeButton.innerHTML = '<i class="fas fa-trash-alt"></i>';
            removeButton.onclick = function () {
                // Remove the user from the array
                selectedUsersArray = selectedUsersArray.filter(user => user !== userID);

                // Update the FormData
                updateFormData();

                selectedUsersDiv.removeChild(card);
            };

            cardBody.appendChild(removeButton);
            card.appendChild(cardBody);
            selectedUsersDiv.appendChild(card);

            // Clear search input and reset options display
            document.getElementById('searchInput').value = "";
            for (var i = 0; i < userList.options.length; i++) {
                userList.options[i].style.display = "";
            }
        }
    }
}
function searchCategories() {
    var input, filter, categoryList, options, option, i, txtValue, found = false;
    input = document.getElementById('searchCategory');
    filter = input.value.toUpperCase();
    categoryList = document.getElementById('categoryList');
    options = categoryList.getElementsByTagName('option');

    for (i = 0; i < options.length; i++) {
        option = options[i];
        txtValue = option.textContent || option.innerText;

        if (!found && txtValue.toUpperCase().indexOf(filter) > -1) {
            // If not found yet, make the option the selected option
            categoryList.selectedIndex = i;
            found = true;
        }

        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            option.style.display = "";
        } else {
            option.style.display = "none";
        }
    }
}

function addCategory() {
    var selectedCategories = document.getElementById('selectedCategories');
    var categoryList = document.getElementById('categoryList');
    var selectedOption = categoryList.options[categoryList.selectedIndex];
    if (selectedOption) {
        var userName = selectedOption.text;
        var userID = Number(selectedOption.value);

        // Check if the user is already selected
        if (!selectedCategoriesArray.includes(userID)) {
            // Add the user to the array
            selectedCategoriesArray.push(userID);

            // Update the FormData
            updateFormData();

            var card = document.createElement('div');
            card.className = 'card mb-2 mr-2';

            var cardBody = document.createElement('div');
            cardBody.className = 'card-body d-flex flex-row align-items-center';

            var userNameText = document.createTextNode(userName);
            cardBody.appendChild(userNameText);

            var removeButton = document.createElement('button');
            removeButton.className = 'border-0 bg-transparent';
            removeButton.innerHTML = '<i class="fas fa-trash-alt"></i>';
            removeButton.onclick = function () {
                // Remove the user from the array
                selectedCategoriesArray = selectedCategoriesArray.filter(user => user !== userID);

                // Update the FormData
                updateFormData();

                selectedCategories.removeChild(card);
            };

            cardBody.appendChild(removeButton);
            card.appendChild(cardBody);
            selectedCategories.appendChild(card);

            // Clear search input and reset options display
            document.getElementById('searchCategory').value = "";
            for (var i = 0; i < categoryList.options.length; i++) {
                categoryList.options[i].style.display = "";
            }
        }
    }
}


// Use input event instead of change event for real-time updates during typing
document.getElementById('searchInput').addEventListener('input', function () {
    searchUsers();
});

// Use click event instead of change event for real-time updates during typing
document.getElementById('userList').addEventListener('click', function () {
    addUser();
});

document.getElementById('searchCategory').addEventListener('input', function () {
    searchCategories();
});

// Use click event instead of change event for real-time updates during typing
document.getElementById('categoryList').addEventListener('click', function () {
    addCategory();
});
function updateFormData() {
    var formData = new FormData(document.getElementById('createWorkspaceForm'));
    formData.set('selectedUsers', selectedUsersArray);
    formData.set('selectedCategories', selectedCategoriesArray);
}
document.addEventListener('DOMContentLoaded', function () {
    updateFormData();
});