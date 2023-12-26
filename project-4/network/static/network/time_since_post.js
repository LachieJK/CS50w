// Selecting all elements with the class 'time-since-post'
const timeSincePostElements = document.querySelectorAll('.time-since-post');

// Iterating through each element
timeSincePostElements.forEach(element => {
    // Extracting the timestamp when the post/comment was created from the 'data-created' attribute
    const createdTimestamp = new Date(element.getAttribute('data-created')).getTime();
    // Getting the current timestamp
    const currentTimestamp = new Date().getTime();
    // Calculating the time difference between the current time and the time the post/comment was created
    const timeDifference = currentTimestamp - createdTimestamp;
    // Calculating the days, hours, and minutes from the time difference
    const days = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
    const hours = Math.floor((timeDifference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((timeDifference % (1000 * 60 * 60)) / (1000 * 60));
    // Create empty string variable for the time-since-post data
    let displayText = '';

    // Constructing the display text based on the calculated time difference
    if (days === 1) {
        displayText += '1 day';
    } else if (days > 1) {
        displayText += `${days} days`;
    }

    if (days > 0 && (hours > 0 || minutes > 0)) {
        displayText += ', ';
    }

    if (hours === 1) {
        displayText += '1 hour';
    } else if (hours > 1) {
        displayText += `${hours} hours`;
    }

    if ((days > 0 || hours > 0) && minutes > 0) {
        displayText += ', ';
    }

    if (days === 0 && minutes === 1) {
        displayText += '1 minute';
    } else if (minutes > 1) {
        displayText += `${minutes} minutes`;
    }

    if (!days && !hours && !minutes) {
        displayText = 'less than a minute';
    }

    // Setting the formatted display text as the content of the respective element
    element.innerText = displayText + ' ago';
});