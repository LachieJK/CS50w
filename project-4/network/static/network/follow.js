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

// Code that runs after the DOM content is fully loaded
document.addEventListener('DOMContentLoaded', function() {

    // Get elements for follow and unfollow buttons and followers count display
    const followButton = document.getElementById('followBtn');
    const unfollowButton = document.getElementById('unfollowBtn');
    const followersCount = document.getElementById('followers_count');

    // If the follow button exists, add click event listener
    if (followButton) {
        followButton.addEventListener('click', () => {
            // Send a POST request to follow the user
            fetch(`/follow/${profileUserId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken') // Include CSRF token from cookies for security
                }
            })
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Failed to follow user');
                }
            })
            .then(data => {
                followersCount.innerHTML = data.count; // Update followers count in the UI
                location.reload(); // Reload the page to update UI
            });
        });
    }

    // If the unfollow button exists, add click event listener
    if (unfollowButton) {
        unfollowButton.addEventListener('click', () => {
            // Send a POST request to unfollow the user
            fetch(`/follow/${profileUserId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken') // Include CSRF token from cookies for security
                }
            })
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Failed to unfollow user');
                }
            })
            .then(data => {
                followersCount.innerHTML = data.count; // Update followers count in the UI
                location.reload(); // Reload the page to update UI
            });
        });
    }

});
