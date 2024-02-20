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

// Listen for the DOMContentLoaded event to ensure the script runs after the entire DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Get the element with id 'sortable-tasks' to make it sortable
    let sortableList = document.getElementById('sortable-tasks');
    // Initialize the sortable functionality with specific options
    new Sortable(sortableList, {
        swapThreshold: 1, // The threshold of the swap zone
        handle: '.handle', // CSS class used as the drag handle
        animation: 200, // Animation speed in milliseconds
        onEnd: function () { // Callback function when sorting is completed
            // Initialize an array to store the order of task IDs
            var ids = [];
            // Loop through each task element and get its data-id attribute
            sortableList.querySelectorAll('.task-contents').forEach(function (taskElement) {
                ids.push(taskElement.getAttribute('data-id'));
            });
    
            // Send the new order of task IDs to the server via POST request
            fetch('/update-order/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'), // Include CSRF token for security
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    'type': 'task', // Specify the type as task for the server to process
                    'order': ids // The new order of task IDs
                })
            }).then(response => response.json())
            .then(data => console.log(data)); // Log the response data to the console
        }
    });
});

// Listen for the DOMContentLoaded event for the second part of the script
document.addEventListener('DOMContentLoaded', function() {
    // Get the element with id 'sortable-lists' to make the lists sortable
    let sortableList = document.getElementById('sortable-lists');
    // Initialize the sortable functionality with specific options for lists
    new Sortable(sortableList, {
        swapThreshold: 1, // The threshold of the swap zone
        handle: '.handle', // CSS class used as the drag handle
        animation: 200, // Animation speed in milliseconds
        onEnd: function () { // Callback function when sorting is completed
            // Initialize an array to store the order of list IDs
            var ids = [];
            // Loop through each list element and get its data-id attribute
            sortableList.querySelectorAll('.list-contents').forEach(function (listElement) {
                ids.push(listElement.getAttribute('data-id'));
            });
    
            // Send the new order of list IDs to the server via POST request
            fetch('/update-order/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'), // Include CSRF token for security
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    'type': 'list', // Specify the type as list for the server to process
                    'order': ids // The new order of list IDs
                })
            }).then(response => response.json())
            .then(data => console.log(data)); // Log the response data to the console
        }
    });
});
