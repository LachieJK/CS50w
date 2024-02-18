from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    picture = models.ImageField(upload_to='profile-pics', default='profile-pics/default.jpg')


class List(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lists_owned")
    collaborators = models.ManyToManyField(User, related_name="collaborations", blank=True)
    timeCreated = models.DateTimeField(auto_now_add=True)
    listName = models.CharField(max_length=200)

    def total_task_count(self):
        return self.tasks.count()
    
    def completed_task_count(self):
        return self.tasks.filter(completedStatus=True).count()
    
    def issue_task_count(self):
        return self.tasks.filter(issueStatus=True).count()
    

class Task(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name="tasks")
    description = models.TextField()
    timeCompleted = models.DateTimeField(null=True, blank=True)
    completedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="completed_by", null=True, blank=True)
    completedStatus = models.BooleanField(default=False)
    timeAlertedIssue = models.DateTimeField(null=True, blank=True)
    alertedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="alerted_by", null=True, blank=True)
    issueStatus = models.BooleanField(default=False)
    importantFlag = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ['order']  # This ensures tasks are ordered by this field by default.

    def __str__(self):
        return f"Task {self.id}: '{self.description}' is apart of the {self.list.listName} list."
    

class Issue(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="issue")
    severity = models.TextField()
    importance = models.TextField()
    description = models.TextField()
    reportedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reported_by", null=True, blank=True)
    timeReported = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    timeResolved = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"The issue '{self.description}' of severity {self.severity} is related to the task '{self.task.description}'"

