document.addEventListener('DOMContentLoaded', function() {
    let sortableList = document.getElementById('sortable-list');
    new Sortable(sortableList, {
        swapThreshold: 1,
        handle: '.handle', // handle class
        animation: 200
    });
});