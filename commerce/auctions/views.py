from django.contrib.auth import authenticate, login, logout
from django import forms
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from .models import User, Category, Bid, Auction_list, WatchList, Comment
@login_required
def profile(request):
    return render(request,"auctions/profile/profile.html",{
        "counter_active_auctions": Auction_list.objects.filter(bid__in = Bid.objects.filter(user = request.user), state_bid = True).count(),
        "counter_non_active_auctions": Auction_list.objects.filter(bid__in = Bid.objects.filter(user = request.user), state_bid = False).count(),
        "counter_won_auctions":Auction_list.objects.filter(last_bidder = request.user, state_bid = False).exclude(number_bids = 1).count()
    })

@login_required
def active_auctions(request):
    bids = Bid.objects.filter(user = request.user)
    active_auctions = Auction_list.objects.filter(bid__in = bids, state_bid = True)
    # if ul se face in html (daca bid ul este al persoanei)
    return render(request, "auctions/profile/active_auctions.html",{
        "active_auctions": active_auctions
    })
@login_required
def non_active_auctions(request):
    bids = Bid.objects.filter(user = request.user)
    non_active_auctions = Auction_list.objects.filter(bid__in = bids, state_bid = False)
    # if ul se face in html (daca bid ul este al persoanei)
    return render(request, "auctions/profile/non_active_auctions.html",{
        "non_active_auctions": non_active_auctions
    })

@login_required
def won_auctions(request):
    
    won_auctions = Auction_list.objects.filter(last_bidder = request.user, state_bid = False).exclude(number_bids = 1)
    # if ul se face in html (daca bid ul este al persoanei)
    return render(request, "auctions/profile/won_auctions.html",{
        "won_auctions": won_auctions
    })

def index(request):
    return render(request, "auctions/index.html",{
        "auction_list":Auction_list.objects.all().exclude(state_bid = False)
    })


def watchList(request):
    
    return render(request, "auctions/watchlist.html", {
        "elements": WatchList.objects.filter(user = request.user)
    })

def get_watchlist_count(request):
    if request.user.is_authenticated:
        counter = WatchList.objects.filter(user = request.user).count()
        return {
            'counter':counter
        }
    else :
        return {
        'counter': None
        }

def auction( request, auction_id ):
    auction = Auction_list.objects.get(pk=auction_id)
    
    
    if request.user.is_authenticated and  WatchList.objects.filter(auction = auction,user = request.user).first() :
        add_remove = "Watchlist -" #remove
        watchlist_object = WatchList.objects.get(auction = auction,user = request.user)
        
    else:
        add_remove = "Watchlist +"
        watchlist_object = None

    if request.method == "POST":
        #verify watchlist
        try:
            if request.POST['watchlist'] == 'Watchlist -': #daca a apasat pe butonul de watchlist
                if watchlist_object:
                    watchlist_object.delete() #daca exista da delete la el
                    add_remove = "Watchlist +"
            elif request.POST['watchlist'] == 'Watchlist +':
                if not WatchList.objects.filter(auction = auction,user = request.user).first(): #daca nu exista in baza de date deja
                    new_watchList_object = WatchList(user = request.user, auction= auction) #daca nu exista, creaza un nou watchlist pt user
                    new_watchList_object.save()
                    add_remove = "Watchlist -"
                    #add a counter of elements in watchlist.
        except:
            pass

        try:
            bid_price = int(request.POST["place_bid"])
            #add bid price
            if bid_price > auction.current_price:
                auction.current_price = bid_price
                auction.number_bids +=1
                auction.last_bidder = request.user
                auction.save()
        except:
            pass

        try:
            new_comment = request.POST["new_comment"]
            if not Comment.objects.filter(comment_text = new_comment,user= request.user).first():
                comment = Comment(user = request.user, auction = auction, comment_text = new_comment)
                comment.save()
        except:
            pass

        try:
            if request.POST['Close_auction']:
                auction.state_bid = False
                auction.save()
                WatchList.objects.filter(auction= auction).delete()

        except:
            pass
    


    return render(request, "auctions/auction.html",{
        "auction":auction,
        "add_remove":add_remove,
        "comments": Comment.objects.filter(auction = auction).order_by('-id')
    })

class CreateNewBidForm(forms.Form):

    title=forms.CharField(label="Title",widget=forms.TextInput(attrs={'placeholder': 'Choose your title'}))
    text=forms.CharField(widget= forms.Textarea(attrs={'rows':4, 'cols':20,'placeholder': 'Write details about your bid'}), label="Text")
    startBid = forms.IntegerField(min_value=1,max_value=1000000,widget=forms.NumberInput(attrs={'placeholder': 'Write a price in PENCILS'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(),widget = forms.Select)
    URL = forms.URLField(label='Your picture link', required=False,widget=forms.URLInput(attrs={'placeholder': 'e.g. https://loll.com/12.jpg'}))

@login_required
def create(request):

    if request.method == "POST":
        form = CreateNewBidForm(request.POST)
        if form.is_valid():
            #(optional) sa facem o verficare daca titlul este la fel ca altele.
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]
            startBid = form.cleaned_data["startBid"]
            URL = form.cleaned_data["URL"]
            category = form.cleaned_data["category"]
            bid = Bid(user = request.user, title = title, text = text, startBid = startBid, URL = URL,category=category)
            bid.save()
            auction = Auction_list(bid = bid, last_bidder = request.user, current_price = bid.startBid)
            auction.save()
            messages.info(request,'Successfully created a bid, congrats!')
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html",{
            "form":CreateNewBidForm()
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
