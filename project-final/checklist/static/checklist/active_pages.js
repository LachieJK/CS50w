// Get the current page's path from the window location
const activePage = window.location.pathname;
// Select all anchor tags inside a nav element and iterate over them
const navLinks = document.querySelectorAll('nav a').forEach(link => {
    // Define an array of paths to exclude from the active class assignment
    const excludePaths = ['/login', '/register', '/checklist'];
    // Check if the current link's href attribute contains the active page's path and ensure it does not include any of the paths we want to exclude
    if (link.href.includes(activePage) && !excludePaths.some(excludePath => link.href.includes(excludePath))) {
        // If conditions are met, add the 'active' class to highlight the link as active
        link.classList.add('active');
    }
});
