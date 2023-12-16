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

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

}

function send_email(event) {
  event.preventDefault();

    console.log('sees the submitted form');

    // Make a POST request using fetch
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: document.querySelector('#compose-recipients').value,
          subject: document.querySelector('#compose-subject').value,
          body: document.querySelector('#compose-body').value
      })
    })
    .then(emails => {
      // Logs the email status response (i.e., sent successfully)
      console.log(emails);
      // Load the 'sent' mailbox or perform other actions as needed
      load_mailbox('sent');
  });
}

function load_mailbox(mailbox) {

document.getElementById('email-placeholder').innerHTML = '';

  const emailPlaceholder = document.getElementById('email-placeholder');
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-heading').innerHTML = `${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}`;

  //Retrieve all mail from that inbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Logs all the emails
      console.log(emails);
      if (emails.length === 0) {
        emailPlaceholder.innerHTML = '<p class="empty-inbox">Inbox is Empty</p>'
      }
      else {
        emails.forEach(email => {

          //Create all the divs to display the contents of each email
          const emailContainer = document.createElement("div");
          if (email.read === true) {
            emailContainer.className = 'email-container-read';
          }
          else {
            emailContainer.className = 'email-container-unread';
          }
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
  
          //Fill out the divs with the associative content
          if (mailbox === 'sent') {
            emailAddress.innerHTML = `To ${email['recipients']}`;
          }
          else {
            emailAddress.innerHTML = `From ${email['recipients']}`;
          }
          emailSubject.innerHTML = `<b>${email['subject']}</b>`;
          emailSeperator.innerHTML = ' - ';
          emailBody.innerHTML = email.body;
          emailDate.innerHTML = `<i>${email['timestamp']}</i>`;
          
          //Append the divs to html
          emailPlaceholder.appendChild(emailContainer);
          emailContainer.appendChild(emailAddress);
          emailContainer.appendChild(emailContents);
          emailContainer.appendChild(emailDate);
          emailContents.appendChild(emailSubject);
          emailContents.appendChild(emailSeperator);
          emailContents.appendChild(emailBody);
        });
      }
  });
}

