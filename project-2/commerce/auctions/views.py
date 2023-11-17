from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from decimal import Decimal

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
        if not request.user.is_authenticated:
            return redirect('error', message="Must be signed in to create a listing")
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.POST.get('url')
        category_name = request.POST.get('category')
        if not image.strip():
            image = 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.stack.imgur.com%2Fy9DpT.jpg&f=1&nofb=1&ipt=65fd893c5b83c58d8fa2af05c63703caffeecceb1e383b5b7c7fccc73fed228d&ipo=images'
        if not title.strip() or not description.strip() or not price.strip() or not category_name.strip():
            return redirect('error', message="Not all required fields were filled correctly")
        category_instance = Category.objects.get(name=category_name)
        listing = Listings(name = title, description = description, category = category_instance, owner = request.user, price = price, image = image)
        listing.save()
        return redirect('index');

def category(request, category_id):
    return render(request, "auctions/category.html", {
        "listings": Listings.objects.filter(category=category_id).order_by('-created'),
        "categories": Category.objects.all().order_by('name'),
        "title": Category.objects.get(id=category_id).name
    })

def listing(request, listing_id):
    if request.method == 'GET':
        listing = get_object_or_404(Listings, pk = listing_id)
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "categories": Category.objects.all().order_by('name')
        })
    else:
        if "bid" in request.POST:
            price_str = request.POST.get('bid')
            if not price_str.strip():
                return redirect('error', message="Must enter a numeric bid value")
            try:
                price = Decimal(price_str)
            except ValueError:
                return redirect('error', message="Invalid bid value")
            if price <= Listings.objects.get(id=listing_id).current_price():
                return redirect('error', message="Bid must be larger than the current price")
            bid = Bids(user = request.user, item = Listings.objects.get(id=listing_id), new_price = price)
            bid.save()
            listing = get_object_or_404(Listings, pk = listing_id)
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "categories": Category.objects.all().order_by('name')
            })
        if "close-listing" in request.POST:
            listing = Listings.objects.get(id=listing_id)
            listing.active = False
            listing.save()
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "categories": Category.objects.all().order_by('name')
            })

def error(request, message):
    return render(request, "auctions/error.html", {
        "message": message
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
        return render(request, "auctions/login.html", {
            "categories": Category.objects.all().order_by('name')
        })


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
        return render(request, "auctions/register.html", {
            "categories": Category.objects.all().order_by('name')
        })
