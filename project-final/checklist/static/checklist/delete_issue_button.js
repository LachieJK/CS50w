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

// Wait for the DOM to be fully loaded before running the script
document.addEventListener('DOMContentLoaded', function() {
    // Select all SVG elements within elements with class 'delete-issue-buttons'
    const binIcons = document.querySelectorAll('.delete-issue-buttons svg');
    // Add a click event listener to each bin icon
    binIcons.forEach(binIcon => {
        binIcon.addEventListener('click', function() {
            // Get the button (is the immediate parent of the SVG)
            const button = binIcon.parentElement;
            // Retrieve the task ID from the data-task-id attribute
            const issueId = button.getAttribute('data-issue-id');
            // Send a POST request to the server to delete the issue
            fetch(`/delete-issue/${issueId}`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'), // Use the getCookie function to get the CSRF token value
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json()) // Parse the JSON response
            .then(data => {
                if (data.success) {
                    // If the server responded with success, reload the page
                    window.location.reload();
                }
            });
        });
    });
});