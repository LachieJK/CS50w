from django.contrib.auth.models import AbstractUser
from django.db import models

# Extends the AbstractUser to add custom fields to the User model
class User(AbstractUser):
    picture = models.ImageField(upload_to='profile-pics', default='profile-pics/default.jpg')  # Profile picture for the user

# Model for a list, which can have many tasks and collaborators
class List(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lists_owned")  # The owner of the list
    collaborators = models.ManyToManyField(User, related_name="collaborations", blank=True)  # Users who collaborate on the list
    timeCreated = models.DateTimeField(auto_now_add=True)  # Timestamp for when the list was created
    listName = models.CharField(max_length=200)  # Name of the list
    order = models.PositiveIntegerField(default=0, blank=False, null=False)  # Order in which the list appears

    # Returns the total number of tasks in the list
    def total_task_count(self):
        return self.tasks.count()
    
    # Returns the count of completed tasks in the list
    def completed_task_count(self):
        return self.tasks.filter(completedStatus=True).count()
    
    # Returns the count of tasks with issues in the list
    def issue_task_count(self):
        return self.tasks.filter(issueStatus=True).count()

# Model for tasks within a list
class Task(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name="tasks")  # The list to which the task belongs
    description = models.TextField()  # Description of the task
    timeCompleted = models.DateTimeField(null=True, blank=True)  # Timestamp for when the task was completed
    completedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="completed_by", null=True, blank=True)  # User who completed the task
    completedStatus = models.BooleanField(default=False)  # Flag indicating if the task is completed
    timeAlertedIssue = models.DateTimeField(null=True, blank=True)  # Timestamp for when an issue was reported
    alertedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="alerted_by", null=True, blank=True)  # User who reported an issue
    issueStatus = models.BooleanField(default=False)  # Flag indicating if the task has an issue
    importantFlag = models.BooleanField(default=False)  # Flag indicating if the task is marked as important
    order = models.PositiveIntegerField(default=0, blank=False, null=False)  # Order in which the task appears within its list

    class Meta:
        ordering = ['order']  # Ensures tasks are ordered by the 'order' field by default.

    def __str__(self):
        # String representation of the Task model
        return f"Task {self.id}: '{self.description}' is apart of the {self.list.listName} list."

# Model for issues reported on tasks
class Issue(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="issue")  # The task to which the issue belongs
    severity = models.TextField()  # Severity of the issue
    importance = models.TextField()  # Importance of resolving the issue
    description = models.TextField()  # Description of the issue
    reportedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reported_by", null=True, blank=True)  # User who reported the issue
    timeReported = models.DateTimeField(auto_now_add=True, null=True, blank=True)  # Timestamp for when the issue was reported
    timeResolved = models.DateTimeField(null=True, blank=True)  # Timestamp for when the issue was resolved

    def __str__(self):
        # String representation of the Issue model
        return f"The issue '{self.description}' of severity {self.severity} is related to the task '{self.task.description}'"


