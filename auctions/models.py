from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime


class User(AbstractUser):
    pass


class Category(models.Model):
    type = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.type}"

class bid(models.Model):
    bid_user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name="buser")
    price = models.FloatField(default=0)

    def __str__(self):
        return f"{self.bid_user} : {self.price}"

class listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    image = models.CharField(max_length=1000 , blank=True,null= True)
    price = models.ForeignKey(bid,on_delete=models.CASCADE,null=True,related_name="bid_price")
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="user",blank=True,null=True)
    categories = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="category",null=True)
    is_active = models.BooleanField(default=True,null=True,blank=True)
    watchlist = models.ManyToManyField(User,related_name="watchlist",null=True,blank=True)
    

    def __str__(self):
        return f"{self.title} "

class comment(models.Model):
    Comment_user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name="comment_user")
    comment = models.CharField(max_length=300,null=True)
    item = models.ForeignKey(listing,on_delete=models.CASCADE,related_name="comment_item",null=True)
    time = models.DateTimeField(default=datetime.datetime.now(),null=True)

    def __str__(self):
        return f"{self.Comment_user} comment on {self.item} : {self.comment}"
    