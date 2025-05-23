from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=100)
    CONDITIONS = [
        ('Brand New', 'Brand New'),
        ('Lightly Used', 'Lightly Used'),
        ('Moderately Used', 'Moderately Used'),
        ('Heavily Used', 'Heavily Used')
    ]
    condition = models.CharField(max_length=20,choices=CONDITIONS)
    image = models.URLField(max_length=2000)
    description = models.CharField(max_length=2000)
    CATEGORIES = [
        ('Home', 'Home'),
        ('Fashion', 'Fashion'),
        ('Toys', 'Toys'),
        ('Electronics', 'Electronics'),
        ('Education', 'Education'),
        ('Others', 'Others')
    ]
    category = models.CharField(max_length=30, choices=CATEGORIES)
    datetime = models.DateTimeField(auto_now_add=True)
    initial_price = models.DecimalField(max_digits=8, decimal_places=2)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    def save(self, *args, **kwargs):
        if not self.pk:  # This means the instance is not saved yet (it's new)
            self.price = self.initial_price
        if self.price < self.initial_price:
            raise ValueError("Price cannot be less than the initial price")
        super().save(*args, **kwargs)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing")
    closed = models.BooleanField(default=False)

class Watchlist(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchlist_listing")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist_user")
    datetime = models.DateTimeField(auto_now_add=True)


class Bid(models.Model):
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids", null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    datetime = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    text = models.CharField(max_length=5000)
    datetime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments", null=True)
    removed = models.BooleanField(default=False)
