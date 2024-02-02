// Adding event listener to each '.view-list' element
document.querySelectorAll('.view-list').forEach(function(element) {
    element.addEventListener('click', function() {
        // Retrieving the URL associated with the listing and navigating to it
        var listUrl = this.getAttribute('data-list-url');
        window.location.href = listUrl;
    });
});