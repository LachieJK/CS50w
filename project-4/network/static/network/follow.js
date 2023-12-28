function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function() {

    const followButton = document.getElementById('followBtn');
    const unfollowButton = document.getElementById('unfollowBtn');
    const followersCount = document.getElementById('followers_count');

    if (followButton) {
        followButton.addEventListener('click', () => {
            fetch(`/follow/${profileUserId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken') // Including CSRF token from cookies
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
                location.reload();
            });
        });
    }
    if (unfollowButton) {
        unfollowButton.addEventListener('click', () => {
            fetch(`/follow/${profileUserId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken') // Including CSRF token from cookies
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
                location.reload();
            });
        });
    }

});
