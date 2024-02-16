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
    const binIcons = document.querySelectorAll('.delete-issue-buttons svg');

    binIcons.forEach(binIcon => {
        binIcon.addEventListener('click', function() {
            // Assuming the button is the immediate parent of the SVG
            const button = binIcon.parentElement;
            // Retrieve the task ID from the data-task-id attribute
            const issueId = button.getAttribute('data-issue-id');
            fetch(`/delete-issue/${issueId}`, {
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
        });
    });
});