from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Max

# Custom user model inheriting from Django's AbstractUser
class User(AbstractUser):
    pass

# Category model representing different categories for listings
class Category(models.Model):
    name = models.CharField(max_length=64)  # Category name

    def __str__(self):
        return self.name  # String representation of the category

# Listings model representing items available for auction
class Listings(models.Model):
    id = models.AutoField(primary_key=True)  # Primary key
    name = models.CharField(max_length=64)  # Name of the listing
    description = models.TextField()  # Description of the listing
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Starting price of the listing
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listings")  # Category of the listing
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")  # Owner of the listing
    created = models.DateTimeField(auto_now_add=True)  # Creation timestamp
    image = models.URLField(max_length=200, verbose_name='Image URL', null=True)  # URL for the image
    active = models.BooleanField(default=True)  # Whether the listing is active
    watched_by = models.ManyToManyField(User, blank=True, related_name="watchlist")  # Users watching this listing

    def __str__(self):
        return f"{self.name} sets are starting price of {self.price} for {self.price}"  # String representation of the listing

    def bid_count(self):
        return self.bids.all().count()  # Number of bids on the listing
    
    def current_price(self):
        if self.bid_count() > 0:
            return round(self.bids.aggregate(Max('new_price'))['new_price__max'], 2)
        else:
            return self.price  # Current price of the listing
    
    def current_winner(self):
        if self.bid_count() > 0:
            return self.bids.get(new_price=self.current_price()).user
        else:
            return None  # Current highest bidder
    
    def in_watchlist(self, user):
        return user.watchlist.filter(pk=self.pk).exists()  # Checks if the user has this listing in their watchlist

# Bids model representing bids made on listings
class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")  # User placing the bid
    item = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="bids")  # Listing being bid on
    new_price = models.DecimalField(max_digits=10, decimal_places=2)  # New price offered in the bid

    def __str__(self):
        return f"{self.user} bid {self.new_price} on {self.item}"  # String representation of the bid

# Comments model representing comments on listings
class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")  # User making the comment
    item = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="comments")  # Listing being commented on
    description = models.TextField()  # Comment content
    date = models.DateTimeField(auto_now_add=True)  # Timestamp when the comment was made

    def __str__(self):
        return f"{self.user} commented {self.description} on {self.item}"  # String representation of the comment
