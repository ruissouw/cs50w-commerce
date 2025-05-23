from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required

def index(request):
    listings = Listing.objects.filter(closed=False)
    if request.method == 'POST':
        category = request.POST.get('categories')
        condition = request.POST.get('condition')
        filters = {'closed': False}
        if category != "Categories":
            filters['category'] = category
        if condition != "Condition":
            filters['condition'] = condition
        listings = Listing.objects.filter(**filters)
    signed_in = request.user.is_authenticated
    return render(request, "auctions/index.html", {
        "listings": listings,
        "signed_in": signed_in
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

@login_required
def create(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        return render(request, "auctions/create.html", {
            "form": form,
            "error": True
         })
    return render(request, "auctions/create.html", {
        "form": CreateListingForm()
    })

def listing_data(request, listing):
    user = request.user
    comments = listing.comments.filter(removed=False)
    winning = False
    watchlist = False
    owner = False
    if listing.user == request.user:
        owner = True
    if request.user.is_authenticated:
        watchlist = Watchlist.objects.filter(listing=listing, user=user).exists()
    all_bids = Bid.objects.filter(listing=listing)
    if all_bids.exists():
        highest_bidder = all_bids.order_by('-amount').first().user
        if highest_bidder == request.user:
            winning = True


    return {
        "listing": listing,
        "watchlist": watchlist,
        "bid_form": BiddingForm(),
        "bids": all_bids.count(),
        "winning": winning,
        "owner": owner,
        "comments": comments,
        "comment_form": CommentForm(),
        "bid_error": False,
        "comment_error": False,
        "placed_bid": False
    }

def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    return render(request, "auctions/listing.html", listing_data(request, listing))

@login_required
def add_to_watchlist(request, listing_id):
    user = request.user
    if request.method == "POST":
        listing = Listing.objects.get(id=listing_id)
        action = request.POST.get("watchlist")
        if action == "Add to watchlist":
            watchlist = Watchlist(listing=listing, user=user)
            watchlist.save()
        elif action == "Remove from watchlist":
            watchlist = Watchlist.objects.get(listing=listing, user=request.user)
            watchlist.delete()
    watchlist = Watchlist.objects.filter(listing=listing, user=user).exists()
    return redirect('listing', listing_id=listing_id)

@login_required
def watchlist(request):
    user = request.user
    watchlists = Watchlist.objects.filter(user=user)
    listings = [watchlist.listing for watchlist in watchlists]
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

@login_required
def bid(request, listing_id):
    user = request.user
    if request.method == "POST":
        listing = Listing.objects.get(id=listing_id)
        form = BiddingForm(request.POST)
        if not form.is_valid():
            context = listing_data(request, listing)
            context["bid_form"] = form
            return render(request, "auctions/listing.html", context)
        bid = form.save(commit=False)
        if bid.amount <= listing.price:
            context = listing_data(request, listing)
            context["bid_form"] = form
            context["bid_error"] = True
            return render(request, "auctions/listing.html", context)
        bid.listing = listing
        bid.user = user
        listing.price = bid.amount
        listing.save()
        bid.save()
        if not Watchlist.objects.filter(user=user, listing=listing).exists():
            watchlist = Watchlist(listing=listing, user=user)
            watchlist.save()
        context = listing_data(request, listing)
        context["placed_bid"] = True
        return render(request, "auctions/listing.html", context)

@login_required
def close(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    if request.method == "POST":
        if request.POST.get("close") == "Close Listing":
            listing.closed = True
            listing.save()
    return redirect('listing', listing_id=listing_id)

@login_required
def comment(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    user = request.user
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.listing = listing
            comment.user = user
            comment.save()
        else:
            context = listing_data(request, listing)
            context["comment_form"] = form
            context["comment_error"] = form
            return render(request, "auctions/listing.html", context)
    return redirect('listing', listing_id=listing_id)

def my_listings(request):
    user = request.user
    actives = Listing.objects.filter(closed=False, user=user)
    closes = Listing.objects.filter(closed=True, user=user)
    closed_all = Listing.objects.filter(closed=True)
    won_listings = []
    for listing in closed_all:
        all_bids = Bid.objects.filter(listing=listing)
        if all_bids.exists():
            highest_bidder = all_bids.order_by('-amount').first().user
            if highest_bidder == request.user:
                won_listings.append(listing)
    print(won_listings)
    return render(request, "auctions/my_listings.html", {
        "actives": actives,
        "closes": closes,
        "won_listings": won_listings
    })
