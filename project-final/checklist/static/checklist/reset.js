// Function to get the value of a specific cookie by name
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        // Split document.cookie at semicolons to get an array of cookies
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie string begins with the name we want
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                // Decode and assign the value of the cookie
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break; // Break the loop once the cookie is found
            }
        }
    }
    return cookieValue; // Return the value of the cookie, or null if not found
}

// Listen for the DOMContentLoaded event to ensure the DOM is fully loaded before executing the script
document.addEventListener('DOMContentLoaded', function() {
    // Attach an onclick event listener to the clear-tasks-button
    document.querySelector('#clear-tasks-button').onclick = function() {
        // Select the clear-tasks-button
        const button = document.querySelector('#clear-tasks-button');
        // Retrieve the list ID stored in the data-list-id attribute of the button
        const listId = button.getAttribute('data-list-id');
        // Send a POST request to the server to clear tasks for the specified list ID
        fetch(`/clear_tasks/${listId}`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'), // Retrieve the CSRF token using the getCookie function
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json()) // Parse the JSON response from the server
        .then(data => {
            if (data.success) {
                // If the server response indicates success, reload the page
                window.location.reload();
            }
        });
    };
});

// Listen for the DOMContentLoaded event to ensure the DOM is fully loaded before executing the script
document.addEventListener('DOMContentLoaded', function() {
    // Attach an onclick event listener to the clear-lists-button
    document.querySelector('#clear-lists-button').onclick = function() {
        // Select the clear-lists-button directly
        const button = document.querySelector('#clear-lists-button');
        // Send a POST request to the server to clear all lists
        fetch('/clear_lists/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'), // Retrieve the CSRF token using the getCookie function
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json()) // Parse the JSON response from the server
        .then(data => {
            if (data.success) {
                // If the server response indicates success, reload the page
                window.location.reload();
            }
        });
    };
});
