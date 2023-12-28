document.addEventListener('DOMContentLoaded', function() {

    const followButton = document.getElementById('followBtn');
    const unfollowButton = document.getElementById('unfollowBtn');
    const followersCount = document.getElementById('followers_count');

    if (followButton) {
        followButton.addEventListener('click', () => {
            fetch(`/follow/${profileUserId}`, {
                method: 'POST'
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
                method: 'POST'
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
