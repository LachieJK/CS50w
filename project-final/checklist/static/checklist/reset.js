// Function to get the value of a specific cookie by name
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie string begins with the name we want
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break; // Break the loop once the cookie is found
            }
        }
    }
    return cookieValue; // Return the value of the cookie, or null if not found
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#clear-tasks-button').onclick = function() {
        const button = document.querySelector('#clear-tasks-button');
        const listId = button.getAttribute('data-list-id');
        fetch(`/clear_tasks/${listId}`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'), // Function to get CSRF token; see note below
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            }
        });
    };
});

document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#clear-lists-button').onclick = function() {
        const button = document.querySelector('#clear-lists-button');
        fetch('/clear_lists/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'), // Function to get CSRF token; see note below
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            }
        });
    };
});