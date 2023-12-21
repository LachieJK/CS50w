from django.contrib.auth.models import AbstractUser
from django.db import models


# Custom user model inheriting from AbstractUser
class User(AbstractUser):
    pass


# Model for Email
class Email(models.Model):
    # Foreign key to User table, linking each email to a user
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="emails")
    # Sender field, also a foreign key to User table
    sender = models.ForeignKey("User", on_delete=models.PROTECT, related_name="emails_sent")
    # Many-to-many relationship with User for recipients
    recipients = models.ManyToManyField("User", related_name="emails_received")
    # Fields for email details
    subject = models.CharField(max_length=255)  # Subject of the email
    body = models.TextField(blank=True)  # Body of the email, can be blank
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp of creation
    read = models.BooleanField(default=False)  # Indicates if the email has been read
    archived = models.BooleanField(default=False)  # Indicates if the email has been archived

    # Method to serialize the Email object into a dictionary
    def serialize(self):
        return {
            "id": self.id,  # Email ID
            "sender": self.sender.email,  # Sender's email
            "recipients": [user.email for user in self.recipients.all()],  # List of recipients' emails
            "subject": self.subject,  # Email subject
            "body": self.body,  # Email body
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),  # Timestamp formatted
            "read": self.read,  # Whether the email is read
            "archived": self.archived  # Whether the email is archived
        }
