from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.utils import timezone

class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length = 64)
    
    def __str__(self):
        return f"{self.name}"
    
    
class Bid(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, default=0, related_name="user_bid")
    title = models.CharField(max_length = 64)
    text = models.CharField(max_length=400)
    startBid = models.PositiveIntegerField()
    URL = models.URLField(max_length=200, blank = True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,default=0, related_name="category")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} {self.startBid}"
    


class Auction_list(models.Model):
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE,default = 0, related_name="auction_bid")
    last_bidder = models.ForeignKey(User,on_delete=models.CASCADE, default=0, related_name="auction_user")
    current_price = models.PositiveIntegerField()
    number_bids = models.PositiveIntegerField(default=1)
    state_bid = models.BooleanField(default=True) #if state = True then the auction is active, else is not_active
    def __str__(self):
        return f"Old : {self.bid}  New : {self.current_price} {self.last_bidder}"

class Comment(models.Model):
    user =  models.ForeignKey(User,on_delete=models.CASCADE, default = 0, related_name="user_comment")
    auction = models.ForeignKey(Auction_list, on_delete=models.CASCADE,default = 0, related_name="comment_bid")
    comment_text = models.CharField(max_length=200)
    date_post = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.auction.bid} what : {self.comment_text} when : {self.date_post}"
    
class WatchList(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, default = 0, related_name="user_watchlist")
    auction = models.ForeignKey(Auction_list, on_delete=models.CASCADE, related_name="watchlist_auction")

    def __str__(self):
        return f"User : {self.user} wants {self.bid}" 