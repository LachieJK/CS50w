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

// This function runs after the DOM content is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Select all heart icon elements
    const heartIcons = document.querySelectorAll('.heart i');

    // Iterate over each heart icon
    heartIcons.forEach(heartIcon => {
        // Get the post ID associated with the heart icon
        const postId = heartIcon.closest('.heart').dataset.postId;
        // Create a unique storage key for each post and user
        const storageKey = `liked_${postId}_by_${window.userId}`;
        // Check if the user is authenticated
        const isAuthenticated = window.isAuthenticated === 'True';

        // If the post is already liked by this user, add the 'liked' class to the heart icon
        if (localStorage.getItem(storageKey) === 'true') {
            heartIcon.classList.add('liked');
        }

        // If the user is authenticated, add event listeners to heart icons
        if (isAuthenticated) {
            heartIcon.addEventListener('click', function() {
                // Get the post ID and like counter element for the clicked heart icon
                const postId = this.closest('.heart').dataset.postId;
                const likeCounter = document.querySelector(`[data-like-counter="${postId}"]`);
                // Retrieve the liked status from local storage
                let liked = localStorage.getItem(storageKey) === 'true';

                // Send a POST request to the server to toggle the like status
                fetch(`/likes/${postId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken') // Include CSRF token for security
                    },
                    body: JSON.stringify({ 
                        action: 'toggle_like' 
                    })
                })
                .then(response => {
                    // Check if the request was successful
                    if (response.ok) {
                        return response.json();
                    } else {
                        throw new Error('Failed to update likes');
                    }
                })
                .then(post => {
                    // Update the UI based on the new like status
                    if (!liked) {
                        heartIcon.classList.add('liked');
                        liked = true;
                    } else {
                        heartIcon.classList.remove('liked');
                        liked = false;
                    }
                    // Update the local storage with the new like status
                    localStorage.setItem(storageKey, liked.toString());
                    // Update the likes counter in the UI
                    likeCounter.textContent = post.likes;
                });
            });
        } else {
            // If the user is not authenticated, disable interaction with the heart icon
            heartIcon.style.cursor = 'default';
            heartIcon.style.color = '#a7a7a7';
        }
    });
});

