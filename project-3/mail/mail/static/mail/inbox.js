document.addEventListener('DOMContentLoaded', function() {
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');

});

function compose_email() {
  // Modify classes to change the active state of mailbox elements
  document.getElementById('inbox').classList.remove('active');
  document.getElementById('compose').classList.add('active');
  document.getElementById('sent').classList.remove('active');
  document.getElementById('archived').classList.remove('active');
  // Hide emails-view and email-view, show compose-view
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  // Enable compose fields for recipients and subjects
  document.querySelector('#compose-recipients').disabled = false;
  document.querySelector('#compose-subject').disabled = false;
  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}


function send_email(event) {
  // Prevent the default behavior of the event (e.g., form submission)
  event.preventDefault();
  // Retrieve values from form inputs
  recipients = document.querySelector('#compose-recipients').value;
  subject = document.querySelector('#compose-subject').value;
  body = document.querySelector('#compose-body').value
  // Check for empty subject or body, set placeholders if empty
  if (subject === '') {
    subject = "(No Subject)";
  }
  if (body === '') {
    body = "(No Body)";
  }
  // Make a POST request using fetch to send the email
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body
    })
  })
  .then(response => {
    // Clear any previous messages
    const messagePlaceholder = document.getElementById('message-placeholder');
    messagePlaceholder.innerHTML = '';
    // Create a success message and display it
    const div = document.createElement('div');
    div.className = 'popup';
    div.innerHTML = "Email was Sent Successfully!";
    // Append the success message to the message placeholder
    messagePlaceholder.appendChild(div);
    // Set a timeout to animate and remove the success message after a delay
    setTimeout(() => {
      div.style.animation = 'popup 3s ease-out forwards';
      // Remove the message after the animation ends
      div.addEventListener('animationend', () => {
        div.remove();
      });
    }, 100);
    // Load the 'sent' mailbox after sending the email
    load_mailbox('sent');
  });
}

function load_mailbox(mailbox) {
  // Highlight the selected mailbox and remove highlights from others
  if (mailbox === 'inbox') {
    document.getElementById('inbox').classList.add('active');
    document.getElementById('compose').classList.remove('active');
    document.getElementById('sent').classList.remove('active');
    document.getElementById('archived').classList.remove('active');
  } else if (mailbox === 'sent') {
    document.getElementById('inbox').classList.remove('active');
    document.getElementById('compose').classList.remove('active');
    document.getElementById('sent').classList.add('active');
    document.getElementById('archived').classList.remove('active');
  } else if (mailbox === 'archive') {
    document.getElementById('inbox').classList.remove('active');
    document.getElementById('compose').classList.remove('active');
    document.getElementById('sent').classList.remove('active');
    document.getElementById('archived').classList.add('active');
  }
  // Clear email placeholder
  document.getElementById('email-placeholder').innerHTML = '';
  // Get email placeholder element
  const emailPlaceholder = document.getElementById('email-placeholder');
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  // Show the mailbox name
  document.querySelector('#emails-heading').innerHTML = `${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}`;
  // Retrieve all mail from the selected mailbox
  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      // Log all the emails
      console.log(emails);
      if (emails.length === 0) {
        // Display a message if the mailbox is empty
        emailPlaceholder.innerHTML = `<p class="empty-inbox">${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)} is Empty</p>`;
      } else {
        emails.forEach(email => {
          // Create divs to display the contents of each email
          const emailContainer = document.createElement("div");
          emailContainer.id = email.id;
          emailContainer.className = email.read ? "email-container-read" : "email-container-unread";
          const emailAddress = document.createElement("div");
          emailAddress.className = 'email-address';
          const emailContents = document.createElement("div");
          emailContents.className = 'email-contents';
          const emailSubject = document.createElement("div");
          emailSubject.className = 'email-subject';
          const emailSeperator = document.createElement("div");
          emailSeperator.className = 'email-seperator';
          const emailBody = document.createElement("div");
          emailBody.className = 'email-body';
          const emailDate = document.createElement("div");
          emailDate.className = 'email-date';
          // Fill divs with email content
          if (mailbox === 'sent') {
            emailAddress.innerHTML = `To ${email.recipients}`;
          } else {
            emailAddress.innerHTML = `From ${email.recipients}`;
          }
          emailSubject.innerHTML = `<b>${email.subject}</b>`;
          emailSeperator.innerHTML = ' - ';
          const formattedBody = email.body.replace(/\n/g, '<br>');
          emailBody.innerHTML = formattedBody;
          emailDate.innerHTML = `<i>${email.timestamp}</i>`;
          // Append divs to HTML
          emailPlaceholder.appendChild(emailContainer);
          emailContainer.appendChild(emailAddress);
          emailContainer.appendChild(emailContents);
          emailContainer.appendChild(emailDate);
          emailContents.appendChild(emailSubject);
          emailContents.appendChild(emailSeperator);
          emailContents.appendChild(emailBody);
          // Add event listener to each container (click to view the email)
          document.getElementById(email.id).addEventListener('click', () => load_mail(email));
        });
      }
  });
}

function load_mail(email) {
  // Clear the email view
  const emailPage = document.querySelector('#email-view');
  emailPage.innerHTML = '';
  // Hide other views and display the email view
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  // Create elements to display email content and buttons
  const pageHeadings = document.createElement('div');
  pageHeadings.className = 'page-headings';
  const pageEmailAddresses = document.createElement('div');
  pageEmailAddresses.className = 'page-email-addresses';
  const pageFromAddress = document.createElement('div');
  const pageToAddress = document.createElement('div');
  const pageSubject = document.createElement('div');
  pageSubject.className = 'page-subject';
  const pageTimestamp = document.createElement('div');
  pageTimestamp.className = 'page-timestamp';
  const pageBody = document.createElement('div');
  pageBody.className = 'page-body';
  const pageButtons = document.createElement('div');
  pageButtons.className = 'page-buttons';
  const replyButton = document.createElement('div');
  replyButton.id = `${email.id}-reply`;
  const archiveButton = document.createElement('div');
  archiveButton.id = `${email.id}-archive`;
  // Populate elements with email data
  pageFromAddress.innerHTML = `<b>From: </b>${email.sender}`;
  pageToAddress.innerHTML = `<b>To: </b>${email.recipients}`;
  pageSubject.innerHTML = email.subject;
  pageTimestamp.innerHTML = email.timestamp;
  const formattedBody = email.body.replace(/\n/g, '<br>');
  pageBody.innerHTML = formattedBody;
  // Create buttons and set their content based on email properties
  replyButton.innerHTML = '<button type="button" class="btn btn-primary" style="padding-left: 30px; padding-right: 30px;"><svg xmlns="http://www.w3.org/2000/svg" width="21" height="21" fill="currentColor" class="bi bi-reply-fill" viewBox="0 2 14 14" style="margin-right: 10px;"><path d="M5.921 11.9 1.353 8.62a.719.719 0 0 1 0-1.238L5.921 4.1A.716.716 0 0 1 7 4.719V6c1.5 0 6 0 7 8-2.5-4.5-7-4-7-4v1.281c0 .56-.606.898-1.079.62z"></path></svg>Reply</button>';
  if (email.archived === false) {
    archiveButton.innerHTML = '<button type="button" class="btn btn-danger" style="padding-left: 30px; padding-right: 30px;"><svg xmlns="http://www.w3.org/2000/svg" width="21" height="21" fill="currentColor" class="bi bi-archive-fill" viewBox="0 0 18 18" style="margin-right: 8px;"><path d="M12.643 15C13.979 15 15 13.845 15 12.5V5H1v7.5C1 13.845 2.021 15 3.357 15zM5.5 7h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1 0-1M.8 1a.8.8 0 0 0-.8.8V3a.8.8 0 0 0 .8.8h14.4A.8.8 0 0 0 16 3V1.8a.8.8 0 0 0-.8-.8H.8z"></path></svg>Archive</button>';
  } else {
    archiveButton.innerHTML = '<button type="button" class="btn btn-success" style="padding-left: 30px; padding-right: 30px;"><svg xmlns="http://www.w3.org/2000/svg" width="21" height="21" fill="currentColor" class="bi bi-archive-fill" viewBox="0 0 18 18" style="margin-right: 8px;"><path d="M12.643 15C13.979 15 15 13.845 15 12.5V5H1v7.5C1 13.845 2.021 15 3.357 15zM5.5 7h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1 0-1M.8 1a.8.8 0 0 0-.8.8V3a.8.8 0 0 0 .8.8h14.4A.8.8 0 0 0 16 3V1.8a.8.8 0 0 0-.8-.8H.8z"></path></svg>Unarchive</button>';
  }
  // Append elements to the email view
  emailPage.appendChild(pageHeadings);
  emailPage.appendChild(pageBody);
  emailPage.appendChild(pageButtons)
  pageHeadings.appendChild(pageEmailAddresses);
  pageHeadings.appendChild(pageSubject);
  pageHeadings.appendChild(pageTimestamp);
  pageEmailAddresses.appendChild(pageFromAddress);
  pageEmailAddresses.appendChild(pageToAddress);
  pageButtons.appendChild(replyButton);
  pageButtons.appendChild(archiveButton);
  // Mark the email as read if it's unread
  if (!email.read) {
    fetch(`/emails/${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({ 
        read : true 
      })
    })
  }

  // Event listener for the archive button
  document.getElementById(`${email.id}-archive`).addEventListener('click', () => {
    if (email.archived === false) {
      // If the email is not archived, archive it
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
          archived: true
        })
      })
      .then(response => {
        // Show a message that the email was successfully archived
        const messagePlaceholder = document.getElementById('message-placeholder');
        messagePlaceholder.innerHTML = '';
        const div = document.createElement('div');
        div.className = 'popup';
        div.innerHTML = `The email "${email.subject}" was Archived Successfully!`;
        messagePlaceholder.appendChild(div);
        // Set a timeout to remove the message after the animation ends
        setTimeout(() => {
          div.style.animation = 'popup 3s ease-out forwards';
          div.addEventListener('animationend', () => {
            div.remove();
          });
        }, 100);
        // Load the 'archive' mailbox after archiving the email
        load_mailbox('archive');
      })
    } else {
      // If the email is archived, unarchive it
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
          archived: false
        })
      })
      .then(response => {
        // Show a message that the email was successfully unarchived
        const messagePlaceholder = document.getElementById('message-placeholder');
        messagePlaceholder.innerHTML = '';
        const div = document.createElement('div');
        div.className = 'popup';
        div.innerHTML = `The email "${email.subject}" was Unarchived Successfully!`;
        messagePlaceholder.appendChild(div);
        // Set a timeout to remove the message after the animation ends
        setTimeout(() => {
          div.style.animation = 'popup 3s ease-out forwards';
          div.addEventListener('animationend', () => {
            div.remove();
          });
        }, 100);
        // Load the 'inbox' mailbox after unarchiving the email
        load_mailbox('inbox');
      })
    }
  });

  // Event listener for the reply button
  document.getElementById(`${email.id}-reply`).addEventListener('click', () => {
    // Remove active class from other mailbox buttons and add to compose (assuming it's for writing a new email)
    document.getElementById('inbox').classList.remove('active');
    document.getElementById('compose').classList.add('active');
    document.getElementById('sent').classList.remove('active');
    document.getElementById('archived').classList.remove('active');
    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
    // Clear out composition fields and set initial values for replying to the email
    document.querySelector('#compose-recipients').value = email.recipients;
    document.querySelector('#compose-recipients').disabled = true;
    // Check if the subject already starts with "Re:" and set the subject accordingly
    if (!email.subject.startsWith('Re:')) {
      document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
    } else {
      document.querySelector('#compose-subject').value = email.subject;
    }
    document.querySelector('#compose-subject').disabled = true;
    
    // Set up initial content for the reply email body
    const initialContent = `\n
---------------------------------------------------------------- \n
On ${email.timestamp} ${email.sender} wrote: \n
"${email.body}"`;
    
  document.querySelector('#compose-body').value = initialContent;
  });

}

