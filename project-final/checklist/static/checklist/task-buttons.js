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
    const completeIcons = document.querySelectorAll('.complete-task-buttons svg');

    completeIcons.forEach(completeIcon => {
        completeIcon.addEventListener('click', function() {
            // Assuming the button is the immediate parent of the SVG
            const button = completeIcon.parentElement;
            // Retrieve the task ID from the data-task-id attribute
            const taskId = button.getAttribute('data-task-id');
            const taskDiv = document.getElementById(taskId);
            fetch(`/toggle-completion-status/${taskId}`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'), // Function to get CSRF token; see note below
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log('Issue status toggled successfully:', data.currentStatus);
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
                    setTimeout(function() {
                        window.location.reload();
                    }, 500);
                }
            });
        });
    });
});


document.addEventListener('DOMContentLoaded', function() {
    const issueIcons = document.querySelectorAll('.issue-task-buttons svg');

    issueIcons.forEach(issueIcon => {
        issueIcon.addEventListener('click', function() {
            // Assuming the button is the immediate parent of the SVG
            const button = issueIcon.parentElement;
            // Retrieve the task ID from the data-task-id attribute
            const taskId = button.getAttribute('data-task-id');
            const taskDiv = document.getElementById(taskId);
            fetch(`/toggle-issue-status/${taskId}`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'), // Function to get CSRF token; see note below
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log('Issue status toggled successfully:', data.currentStatus);
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
                    setTimeout(function() {
                        window.location.reload();
                    }, 500);
                }
            });
        });
    });
});