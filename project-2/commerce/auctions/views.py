from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from decimal import Decimal
from django.contrib import messages

from .models import User, Listings, Category, Bids, Comments

def open(request):
    return redirect('index');


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listings.objects.all().order_by('-created'),
        "categories": Category.objects.all().order_by('name')
    })


def create(request):
    if request.method == "GET":
        return render(request, "auctions/create.html", {
            "categories": Category.objects.all().order_by('name')
        })
    else: 
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.POST.get('url')
        category_name = request.POST.get('category')
        if not image.strip():
            image = 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.stack.imgur.com%2Fy9DpT.jpg&f=1&nofb=1&ipt=65fd893c5b83c58d8fa2af05c63703caffeecceb1e383b5b7c7fccc73fed228d&ipo=images'
        if not title.strip() or not description.strip() or not price.strip() or not category_name.strip():
            messages.success(request, "Not all required fields were filled correctly")
            return render(request, "auctions/create.html", {
                "categories": Category.objects.all().order_by('name')
            })
        category_instance = Category.objects.get(name=category_name)
        listing = Listings(name = title, description = description, category = category_instance, owner = request.user, price = price, image = image)
        listing.save()
        messages.success(request, "New listing was created and added to Active Listings")
        return redirect('listing', listing.id);


def category(request, category_id):
    return render(request, "auctions/category.html", {
        "listings": Listings.objects.filter(category=category_id).order_by('-created'),
        "categories": Category.objects.all().order_by('name'),
        "title": Category.objects.get(id=category_id).name
    })


def listing(request, listing_id):
    if request.method == 'GET':
        success = True;
        listing = get_object_or_404(Listings, pk = listing_id)
        watched_by_ids = listing.watched_by.values_list('id', flat=True)
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "categories": Category.objects.all().order_by('name'),
            "comments": Comments.objects.filter(item=listing_id).order_by('-date'),
            "comments_count": Comments.objects.filter(item=listing_id).count(),
            "watched_by_ids": watched_by_ids,
            "success": success
        })
    else:
        listing = get_object_or_404(Listings, pk = listing_id)
        watched_by_ids = listing.watched_by.values_list('id', flat=True)
        if "add-to-watchlist" in request.POST:
            current_user = request.user.id;
            listing = Listings.objects.get(id=listing_id)
            listing.watched_by.add(current_user)
            success = True
            messages.success(request, "Listing has been added to watchlist")
        if "remove-watchlist" in request.POST:
            current_user = request.user.id;
            listing = Listings.objects.get(id=listing_id)
            listing.watched_by.remove(current_user)
            success = True
            messages.success(request, "Listing has been removed from watchlist")
        if "bid" in request.POST:
            price_str = request.POST.get('bid')
            if not price_str.strip():
                success = False
                messages.success(request, "Must enter a numeric bid value")
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "categories": Category.objects.all().order_by('name'),
                    "comments": Comments.objects.filter(item=listing_id).order_by('-date'),
                    "comments_count": Comments.objects.filter(item=listing_id).count(),
                    "watched_by_ids": watched_by_ids,
                    "success": success
                })
            price = Decimal(price_str)
            if price <= Listings.objects.get(id=listing_id).current_price():
                success = False
                messages.success(request, "Bid must be larger than the current price")
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "categories": Category.objects.all().order_by('name'),
                    "comments": Comments.objects.filter(item=listing_id).order_by('-date'),
                    "comments_count": Comments.objects.filter(item=listing_id).count(),
                    "watched_by_ids": watched_by_ids,
                    "success": success
                })
            bid = Bids(user = request.user, item = Listings.objects.get(id=listing_id), new_price = price)
            bid.save()
            success = True
            messages.success(request, "You now have the highest bid for this listing")
        if "close-listing" in request.POST:
            listing = Listings.objects.get(id=listing_id)
            listing.active = False
            listing.save()
            success = True
            messages.success(request, "Your listing is now closed")
        if "comments" in request.POST:
            description = request.POST.get('comments')
            if not description.strip():
                success = False
                messages.success(request, "Must type in the prompt to post a comment")
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "categories": Category.objects.all().order_by('name'),
                    "comments": Comments.objects.filter(item=listing_id).order_by('-date'),
                    "comments_count": Comments.objects.filter(item=listing_id).count(),
                    "watched_by_ids": watched_by_ids,
                    "success": success
                })
            comment = Comments(user = request.user, item = Listings.objects.get(id=listing_id), description = description)
            comment.save()
            success = True
            messages.success(request, "Your comment has now been added")
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "categories": Category.objects.all().order_by('name'),
            "comments": Comments.objects.filter(item=listing_id).order_by('-date'),
            "comments_count": Comments.objects.filter(item=listing_id).count(),
            "watched_by_ids": watched_by_ids,
            "success": success
        })
    

def watchlist(request, user_id):
    if request.method == 'GET':
        return render(request, "auctions/watchlist.html", {
            "listings": Listings.objects.filter(watched_by=user_id).order_by('name'),
            "categories": Category.objects.all().order_by('name')
        })
    else:
        listing_id = request.POST.get('listing_id')
        listing = Listings.objects.get(id=listing_id)
        listing.watched_by.remove(user_id)
        messages.success(request, "Listing was removed from watchlist.")
        return render(request, "auctions/watchlist.html", {
            "listings": Listings.objects.filter(watched_by=user_id).order_by('name'),
            "categories": Category.objects.all().order_by('name')
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
            messages.success(request, "You are now logged in.")
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.success(request, "Invalid username and/or password.")
            return render(request, "auctions/login.html")
    else:
        return render(request, "auctions/login.html", {
            "categories": Category.objects.all().order_by('name')
        })


def logout_view(request):
    logout(request)
    messages.success(request, "You are now logged out.")
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            messages.success(request, "Passwords must match.")
            return render(request, "auctions/register.html")

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.success(request, "Username already taken.")
            return render(request, "auctions/register.html")
        login(request, user)
        messages.success(request, "User has been created, and you are now logged in.")
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html", {
            "categories": Category.objects.all().order_by('name')
        })
