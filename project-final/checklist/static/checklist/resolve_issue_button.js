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

// Listen for the DOMContentLoaded event to ensure the script runs after the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Select all SVG elements within elements with the class 'resolve-issue-buttons'
    const resolveIcons = document.querySelectorAll('.resolve-issue-buttons svg');
    // Iterate over each resolve icon to attach a click event listener
    resolveIcons.forEach(resolveIcon => {
        resolveIcon.addEventListener('click', function() {
            // Assuming the button that needs to be interacted with is the immediate parent of the SVG icon
            const button = resolveIcon.parentElement;
            // Retrieve the issue ID from the data attribute of the button to know which issue to resolve
            const issueId = button.getAttribute('data-issue-id');
            // Send a POST request to the server to resolve the issue with the specified ID
            fetch(`/resolve-issue/${issueId}`, {
                method: 'POST',
                headers: {
                    // Include a CSRF token for security purposes, obtained from a previously defined getCookie function
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json()) // Parse the JSON response from the server
            .then(data => {
                if (data.success) {
                    // If the issue is successfully resolved, reload the page to reflect changes
                    window.location.reload();
                }
            });
        });
    });
});
