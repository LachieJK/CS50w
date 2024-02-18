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
    let sortableList = document.getElementById('sortable-tasks');
    new Sortable(sortableList, {
        swapThreshold: 1,
        handle: '.handle', // handle class
        animation: 200,
        onEnd: function () {
            // Get the order of task IDs
            var ids = [];
            sortableList.querySelectorAll('.task-contents').forEach(function (taskElement) {
                ids.push(taskElement.getAttribute('data-id'));
            });
    
            // Send the new order to the server
            fetch('/update-order/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'), // Function to get CSRF token; see note below
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    'type': 'task',
                    'order': ids
                })
            }).then(response => response.json())
            .then(data => console.log(data));
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    let sortableList = document.getElementById('sortable-lists');
    new Sortable(sortableList, {
        swapThreshold: 1,
        handle: '.handle', // handle class
        animation: 200,
        onEnd: function () {
            // Get the order of list IDs
            var ids = [];
            sortableList.querySelectorAll('.list-contents').forEach(function (listElement) {
                ids.push(listElement.getAttribute('data-id'));
            });
    
            // Send the new order to the server
            fetch('/update-order/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'), // Function to get CSRF token; see note below
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    'type': 'list',
                    'order': ids
                })
            }).then(response => response.json())
            .then(data => console.log(data));
        }
    });
});