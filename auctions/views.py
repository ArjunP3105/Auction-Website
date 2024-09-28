from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import datetime

from .models import User,listing,Category,comment,bid


def index(request):
    return render(request, "auctions/index.html",
                  {
                      "lists":listing.objects.all(),
                      "categories":Category.objects.all()
                  })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create(request):
    if request.method == "GET":
        return render(request,"auctions/create.html",{
        "categories":Category.objects.all(),
        })
    else:
        
        titles = request.POST['title']
        images = request.POST['image']
        users = int(request.POST['username'])
        userinfo = User.objects.get(pk = users)
        descriptions = request.POST['description']
        prices = float(request.POST['price'])
        bids = bid(bid_user = userinfo,price = prices)
        bids.save()
        typeid =  int(request.POST['cate'])
        Cateinfo = Category.objects.get(pk = typeid)
        newlisting = listing(title = titles,description =descriptions,image = images,price = bids,user = userinfo,categories = Cateinfo)
        newlisting.save()
        return HttpResponseRedirect(reverse(index))
    
def category(request):
    if request.method == "POST":
        type_id= request.POST['category_name']
        type = Category.objects.get(pk = type_id)
        return render(request, "auctions/index.html",
                  {
                      "lists":listing.objects.filter(categories = type),
                      "categories":Category.objects.all()
                  })

        
def product(request,id):
    items = listing.objects.get(pk = id)
    watchlisted = request.user in items.watchlist.all()
    user_comment = comment.objects.filter(item = items)
    active = items.is_active
    owner = request.user == items.user
    winner = request.user == items.price.bid_user    
    return render(request,"auctions/product.html",{
        "comments":user_comment,
        "item":items,
        "watchlisted":watchlisted,
        "active":active,
        "owner":owner,
        "winner":winner
     })

def addwatchlist(request,id):
    item = listing.objects.get(pk = id)
    userinfo = request.user
    item.watchlist.add(userinfo)
    return HttpResponseRedirect(reverse("product",args=(id, )))

def removewatchlist(request,id):
    item = listing.objects.get(pk = id)
    userinfo = request.user
    item.watchlist.remove(userinfo)
    return HttpResponseRedirect(reverse("product",args=(id, )))

def watchlist(request):
     currentuser = request.user
     return render(request, "auctions/watchlist.html",
                  {
                      "lists":currentuser.watchlist.all(),
                      "categories":Category.objects.all()
                  })

def Watchcategory(request):
    if request.method == "POST":
        type_id= request.POST['category_name']
        type = Category.objects.get(pk = type_id)
        user = request.user
        return render(request, "auctions/watchlist.html",
                  {
                      "lists":user.watchlist.filter(categories = type),
                      "categories":Category.objects.all()
                  })

def user_comment(request,id):
    if request.method == "POST":
        user_comment = request.POST['comments']
        item_info = listing.objects.get(pk = id)
        curr_user = request.user
        c = comment(Comment_user = curr_user,comment = user_comment, item = item_info)
        c.save()
        return HttpResponseRedirect(reverse("product",args=(id, )))

def biding(request,id):
    if request.method == "POST":
        bidvalue = float(request.POST['price'])
        item_info = listing.objects.get(pk = id)
        curr_bid = float(item_info.price.price)
        user = request.user
        if bidvalue > curr_bid:
            newbid = bid(bid_user = user,price = bidvalue )
            newbid.save()
            item_info.price = newbid
            item_info.save()
            items = listing.objects.get(pk = id)
            watchlisted = request.user in items.watchlist.all()
            active = items.is_active
            owner = request.user == items.user
            winner = request.user == items.price.bid_user
            user_comment = comment.objects.filter(item = items)
            return render(request,"auctions/product.html",{
                "comments":user_comment,
                "item":items,
                "watchlisted":watchlisted,
                "success_message":" Bid Successful ",
                "active":active,
                "owner":owner,
                "winner":winner
            })
        else:
            items = listing.objects.get(pk = id)
            watchlisted = request.user in items.watchlist.all()
            user_comment = comment.objects.filter(item = items)
            active = items.is_active
            owner = request.user == items.user
            winner = request.user == items.price.bid_user
            return render(request,"auctions/product.html",{
                "comments":user_comment,
                "item":items,
                "watchlisted":watchlisted,
                "message":" Unsuccessful: Enter a price greater than the current bid",
                "active":active,
                "owner":owner,
                "winner":winner

            })
def close(request,id):
    if request.method == "POST":
        items = listing.objects.get(pk = id)
        items.is_active = False
        items.save()
        active = items.is_active
        owner = request.user == items.user
        winner = request.user == items.price.bid_user
        watchlisted = request.user in items.watchlist.all()
        user_comment = comment.objects.filter(item = items)
        return render(request,"auctions/product.html",{
            "comments":user_comment,
            "item":items,
            "watchlisted":watchlisted,
            "active":active,
            "owner":owner,
            "winner":winner,
            "close_message":"Auction Successfully closed"
             })


                 
        
