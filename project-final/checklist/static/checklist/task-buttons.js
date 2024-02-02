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
                    if (button.classList.contains('complete')) {
                        button.classList.remove('complete')
                        button.classList.add('not-complete')
                    }
                    else if (button.classList.contains('not-complete')) {
                        button.classList.remove('not-complete')
                        button.classList.add('complete')
                    }
                    window.location.reload();
                    console.log('Completion status toggled successfully:', data.currentStatus);
                    // Optionally toggle classes or update the UI based on the new status
                }
            });
        });
    });
});


document.addEventListener('DOMContentLoaded', function() {
    const completeIcons = document.querySelectorAll('.issue-task-buttons svg');

    completeIcons.forEach(completeIcon => {
        completeIcon.addEventListener('click', function() {
            // Assuming the button is the immediate parent of the SVG
            const button = completeIcon.parentElement;
            // Retrieve the task ID from the data-task-id attribute
            const taskId = button.getAttribute('data-task-id');
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
                    if (button.classList.contains('issue')) {
                        button.classList.remove('issue')
                        button.classList.add('no-issue')
                    }
                    else if (button.classList.contains('no-issue')) {
                        button.classList.remove('no-issue')
                        button.classList.add('issue')
                    }
                    window.location.reload();
                    console.log('Issue status toggled successfully:', data.currentStatus);
                    // Optionally toggle classes or update the UI based on the new status
                }
            });
        });
    });
});