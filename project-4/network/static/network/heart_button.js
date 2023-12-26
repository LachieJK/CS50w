document.addEventListener('DOMContentLoaded', function() {
    const heartIcons = document.querySelectorAll('.heart i');

    heartIcons.forEach(heartIcon => {
        const postId = heartIcon.closest('.heart').dataset.postId;
        const storageKey = `liked_${postId}_by_${window.userId}`; // Unique key for each post and user
        const isAuthenticated = window.isAuthenticated === 'True';

        if (localStorage.getItem(storageKey) === 'true') {
            heartIcon.classList.add('liked');
        }

        if (isAuthenticated) {
            heartIcon.addEventListener('click', function() {
                const postId = this.closest('.heart').dataset.postId;
                const likeCounter = document.querySelector(`[data-like-counter="${postId}"]`);
                const storageKey = `liked_${postId}_by_${window.userId}`;
                let liked = localStorage.getItem(storageKey) === 'true'; // Parse the value as a boolean

                fetch(`/likes/${postId}`, {
                    method: 'POST',
                    body: JSON.stringify({ 
                        action: 'toggle_like' 
                    })
                })
                .then(response => {
                    if (response.ok) {
                        return response.json();
                    } else {
                        throw new Error('Failed to update likes');
                    }
                })
                .then(post => {
                    if (!liked) {
                        heartIcon.classList.add('liked');
                        liked = true;
                    } else {
                        heartIcon.classList.remove('liked');
                        liked = false;
                    }
                    localStorage.setItem(storageKey, liked.toString()); // Store the boolean as a string
                    likeCounter.textContent = post.likes;
                });
            });
        } else {
            heartIcon.style.cursor = 'default';
            heartIcon.style.color = '#a7a7a7';
        }
    });
});
