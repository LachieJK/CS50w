document.addEventListener('DOMContentLoaded', function() {
    const completeIcons = document.querySelectorAll('.complete-task-buttons svg');

    completeIcons.forEach(completeIcon => {
        completeIcon.addEventListener('click', function() {
            // Assuming the button is the immediate parent of the SVG
            const button = completeIcon.parentElement;
            // Retrieve the task ID from the data-task-id attribute
            const taskId = button.getAttribute('data-task-id');
            console.log(taskId); // Log the task ID to verify it's being correctly retrieved - YES

            // Toggle classes on the button, not the SVG
            button.classList.toggle('complete');
            button.classList.toggle('not-complete');
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const completeIcons = document.querySelectorAll('.issue-task-buttons svg');

    completeIcons.forEach(completeIcon => {
        completeIcon.addEventListener('click', function() {
            // Assuming the button is the immediate parent of the SVG
            const button = completeIcon.parentElement;
            // Retrieve the task ID from the data-task-id attribute
            const taskId = button.getAttribute('data-task-id');
            console.log(taskId); // Log the task ID to verify it's being correctly retrieved - YES

            // Toggle classes on the button, not the SVG
            button.classList.toggle('issue');
            button.classList.toggle('no-issue');
        });
    });
});