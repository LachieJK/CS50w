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

  document.getElementById('inbox').classList.remove('active');
  document.getElementById('compose').classList.add('active');
  document.getElementById('sent').classList.remove('active');
  document.getElementById('archived').classList.remove('active');
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

}

function send_email(event) {

  event.preventDefault();

    recipients = document.querySelector('#compose-recipients').value;
    subject = document.querySelector('#compose-subject').value;
    body = document.querySelector('#compose-body').value

    if (subject === '') {
      subject = "(No Subject)";
    }
    if (body === '') {
      body = "(No Body)";
    }

    // Make a POST request using fetch
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: recipients,
          subject: subject,
          body: body
      })
    })
    .then(response => {

      const messagePlaceholder = document.getElementById('message-placeholder');
      messagePlaceholder.innerHTML = '';

      const div = document.createElement('div');
      div.className = 'popup';
      div.innerHTML = "Email was Sent Successfully!";

      messagePlaceholder.appendChild(div);

      setTimeout(() => {
        div.style.animation = 'popup 3s ease-out forwards';

        //Remove the message after the animation ends
        div.addEventListener('animationend', () => {
          div.remove();
        });
      }, 100);

      load_mailbox('sent')

    });
}

function load_mailbox(mailbox) {

  if (mailbox === 'inbox') {
    document.getElementById('inbox').classList.add('active');
    document.getElementById('compose').classList.remove('active');
    document.getElementById('sent').classList.remove('active');
    document.getElementById('archived').classList.remove('active');
  }
  if (mailbox === 'sent') {
    document.getElementById('inbox').classList.remove('active');
    document.getElementById('compose').classList.remove('active');
    document.getElementById('sent').classList.add('active');
    document.getElementById('archived').classList.remove('active');
  }
  if (mailbox === 'archive') {
    document.getElementById('inbox').classList.remove('active');
    document.getElementById('compose').classList.remove('active');
    document.getElementById('sent').classList.remove('active');
    document.getElementById('archived').classList.add('active');
  }

document.getElementById('email-placeholder').innerHTML = '';

  const emailPlaceholder = document.getElementById('email-placeholder');
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
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
        emailPlaceholder.innerHTML = `<p class="empty-inbox">${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)} is Empty</p>`;
      }
      else {
        emails.forEach(email => {

          //Create all the divs to display the contents of each email
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
  
          //Fill out the divs with the associative content
          if (mailbox === 'sent') {
            emailAddress.innerHTML = `To ${email.recipients}`;
          }
          else {
            emailAddress.innerHTML = `From ${email.recipients}`;
          }
          emailSubject.innerHTML = `<b>${email.subject}</b>`;
          emailSeperator.innerHTML = ' - ';
          emailBody.innerHTML = email.body;
          emailDate.innerHTML = `<i>${email.timestamp}</i>`;
          
          //Append the divs to html
          emailPlaceholder.appendChild(emailContainer);
          emailContainer.appendChild(emailAddress);
          emailContainer.appendChild(emailContents);
          emailContainer.appendChild(emailDate);
          emailContents.appendChild(emailSubject);
          emailContents.appendChild(emailSeperator);
          emailContents.appendChild(emailBody);

          //Add event listener to each container (click in to see more about that email)
          document.getElementById(email.id).addEventListener('click', () => load_mail(email));
        });
      }
  });
}

function load_mail(email) {

  const emailPage = document.querySelector('#email-view');
  emailPage.innerHTML = '';

  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

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

  pageFromAddress.innerHTML = `<b>From: </b>${email.sender}`;
  pageToAddress.innerHTML = `<b>To: </b>${email.recipients}`;
  pageSubject.innerHTML = email.subject;
  pageTimestamp.innerHTML = email.timestamp;
  pageBody.innerHTML = email.body;

  emailPage.appendChild(pageHeadings);
  emailPage.appendChild(pageBody);
  pageHeadings.appendChild(pageEmailAddresses);
  pageHeadings.appendChild(pageSubject);
  pageHeadings.appendChild(pageTimestamp);
  pageEmailAddresses.appendChild(pageFromAddress);
  pageEmailAddresses.appendChild(pageToAddress);

  if (!email.read) {
    fetch(`/emails/${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({ read : true })
    })
  }
}

