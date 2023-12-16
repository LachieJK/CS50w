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
  const container = document.querySelector('.email-container');
  
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
      
      emails.forEach(email => {
        const clone = container.cloneNode(true);

        if (mailbox === 'sent') {
          clone.querySelector('.email-address').innerHTML = `To ${email['recipients']}`;
        }
        else {
          clone.querySelector('.email-address').innerHTML = `From ${email['recipients']}`;
        }
        
        clone.querySelector('.email-subject b').innerHTML = email.subject;
        clone.querySelector('.email-body').innerHTML = email.body;
        clone.querySelector('.email-date i').innerHTML = email.timestamp;

        emailPlaceholder.appendChild(clone);
      });
  });
}

