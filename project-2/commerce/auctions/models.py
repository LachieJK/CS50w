from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Listings(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listings")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    created = models.DateTimeField(auto_now_add=True)
    image = models.URLField(max_length=200, verbose_name='Image URL', null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} sets are starting price of {self.price} for {self.price}"

    def bid_count(self):
        return self.bids.all().count()


class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    item = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="bids")
    new_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user} bid {self.new_price} on {self.item}"


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    item = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="comments")
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} commented {self.description} on {self.item}"