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

// Define a function to display a modal for reporting issues for a specific task
function issueModal(taskId) {
    // Select the modal element based on the taskId
    var modal = document.getElementById('reportIssueModal_' + taskId);
    // Initialize a new Bootstrap modal instance
    var modalInstance = new bootstrap.Modal(modal);
    // Listen for the hidden event on the modal to reload the page
    modal.addEventListener('hidden.bs.modal', function () {
        window.location.reload();
    });
    // Show the modal
    modalInstance.show();
}

// Listen for the DOMContentLoaded event to ensure the script runs after the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Select all SVG elements within elements with the class 'complete-task-buttons'
    const completeIcons = document.querySelectorAll('.complete-task-buttons svg');
    // Add a click event listener to each complete icon
    completeIcons.forEach(completeIcon => {
        completeIcon.addEventListener('click', function() {
            // Assume the button is the immediate parent of the SVG
            const button = completeIcon.parentElement;
            // Retrieve the task ID from the data-task-id attribute
            const taskId = button.getAttribute('data-task-id');
            // Select the task div by its ID
            const taskDiv = document.getElementById(taskId);
            // Send a POST request to toggle the completion status of the task
            fetch(`/toggle-completion-status/${taskId}`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'), // Include CSRF token for security
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Log the new issue status
                    console.log('Issue status toggled successfully:', data.currentStatus);
                    // Toggle CSS classes based on the task's new status
                    if (taskDiv.classList.contains('task-completed-with-issue')) {
                        taskDiv.classList.toggle('task-completed-with-issue');
                        taskDiv.classList.toggle('task-issue');
                    }
                    else if (taskDiv.classList.contains('task-issue')) {
                        taskDiv.classList.toggle('task-completed-with-issue');
                    }
                    else {
                        taskDiv.classList.toggle('task-completed');
                    }
                    // Reload the page after a short delay to reflect changes
                    setTimeout(function() {
                        window.location.reload();
                    }, 500);
                }
            });
        });
    });
});

// Listen for the DOMContentLoaded event to ensure the script runs after the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Select all SVG elements within elements with the class 'issue-task-buttons'
    const issueIcons = document.querySelectorAll('.issue-task-buttons svg');

    // Add a click event listener to each issue icon
    issueIcons.forEach(issueIcon => {
        issueIcon.addEventListener('click', function() {
            // Assume the button is the immediate parent of the SVG
            const button = issueIcon.parentElement;
            // Retrieve the task ID from the data-task-id attribute
            const taskId = button.getAttribute('data-task-id');
            // Select the task div by its ID
            const taskDiv = document.getElementById(taskId);
            // Send a POST request to toggle the issue status of the task
            fetch(`/toggle-issue-status/${taskId}`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'), // Include CSRF token for security
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Log the new issue status
                    console.log('Issue status toggled successfully:', data.currentStatus);
                    // Toggle CSS classes based on the task's new issue status
                    if (taskDiv.classList.contains('task-completed-with-issue')) {
                        taskDiv.classList.toggle('task-completed-with-issue');
                        taskDiv.classList.toggle('task-completed');
                    }
                    else if (taskDiv.classList.contains('task-completed')) {
                        taskDiv.classList.toggle('task-completed-with-issue');
                    }
                    else {
                        taskDiv.classList.toggle('task-issue');
                    }
                    // If task has issue, show issue modal; otherwise, reload page
                    if (taskDiv.classList.contains('task-issue') || taskDiv.classList.contains('task-completed-with-issue')) {
                        issueModal(taskId);
                        console.log('Reached here');
                    }
                    else {
                        setTimeout(function() {
                            window.location.reload();
                        }, 500);
                    }       
                }
            });
        });
    });
});

// Listen for the DOMContentLoaded event to ensure the script runs after the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Select all SVG elements within elements with the class 'important-task-buttons'
    const importantIcons = document.querySelectorAll('.important-task-buttons svg');

    // Add a click event listener to each important icon
    importantIcons.forEach(importantIcon => {
        importantIcon.addEventListener('click', function() {
            // Assume the button is the immediate parent of the SVG
            const button = importantIcon.parentElement;
            // Retrieve the task ID from the data-task-id attribute
            const taskId = button.getAttribute('data-task-id');
            // Send a POST request to toggle the important status of the task
            fetch(`/toggle_important/${taskId}`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'), // Include CSRF token for security
                    'Content-Type': 'application/json',
                },
            })
            .then(response => {
                if (response.ok) {
                    // Reload the page to reflect changes if the request was successful
                    window.location.reload();
                } else {
                    // Log error if the request failed
                    console.error('Failed to toggle the important flag.');
                }
            });
        });
    });
});
