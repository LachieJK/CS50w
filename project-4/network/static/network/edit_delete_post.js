document.querySelectorAll('.bi-three-dots').forEach(item => {
    item.addEventListener('click', event => {
        let dropdown = event.target.closest('.post-three-dots').querySelector('.dropdown-menu');
        dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
    });
});

// Clicking outside to close the dropdown
window.onclick = function(event) {
    if (!event.target.matches('.bi-three-dots')) {
    var dropdowns = document.getElementsByClassName("dropdown-menu");
    for (var i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.style.display === "block") {
        openDropdown.style.display = "none";
        }
    }
    }
};
