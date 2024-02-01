// Select all elements with the class '.bi-three-dots' and apply the following function to each
document.querySelectorAll('.bi-three-dots').forEach(item => {
    // Add a click event listener to each item
    item.addEventListener('click', event => {
        // Find the closest parent element with the class '.post-three-dots' 
        // and within it, find the element with the class '.dropdown-menu'
        let dropdown = event.target.closest('.post-three-dots').querySelector('.dropdown-menu');
        // Toggle the display of the dropdown menu: if it's visible (display = 'block'), hide it; if hidden, show it
        dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
    });
});

// Add a click event listener to the entire window (clicking outside the 3 dots will close dropdown)
window.onclick = function(event) {
    // Check if the clicked element does not have the class '.bi-three-dots'
    if (!event.target.matches('.bi-three-dots')) {
        // Get all elements with the class 'dropdown-menu'
        var dropdowns = document.getElementsByClassName("dropdown-menu");
        // Iterate through each dropdown
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            // If the dropdown is currently visible, hide it
            if (openDropdown.style.display === "block") {
                openDropdown.style.display = "none";
            }
        }
    }
};
