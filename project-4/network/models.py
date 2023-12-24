from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    picture = models.ImageField(upload_to='profile-pics', default='profile-pics/default.jpg')

    def __str__(self):
        return self.user.username


class Following(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following") #User of reference (the one who is following)
    user_followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed") #User being followed

    def __str__(self):
        return f"{self.user} follows {self.user_followed}"
    
    def followed_posts(self):
        return self.user_followed.posts.order_by("-timestamp").all()


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    timestamp = models.DateTimeField(auto_now_add=True)
    body = models.TextField(blank=False)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user} posted at {self.timestamp} and has {self.likes} like(s)"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    timestamp = models.DateTimeField(auto_now_add=True)
    body = models.TextField(blank=False)

    def __str__(self):
        return f"{self.user} commented on {self.post.user.username}'s post at {self.timestamp}"