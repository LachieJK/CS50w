from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .models import User, Listings, Category, Bids, Comments

def open(request):
    return redirect('index');

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listings.objects.all() 
    })

def create(request):
    if request.method == "GET":
        unique_categories = set()
        listings = Listings.objects.all()
        for listing in listings:
            if listing.category not in unique_categories:
                unique_categories.add(listing.category)
        return render(request, "auctions/create.html", {
            "categories": unique_categories
        })
    else: 
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.POST.get('url')
        category_name = request.POST.get('category')
        category_instance = Category.objects.get(name=category_name)
        if not title.strip() or not description.strip() or not price.strip():
            return redirect('error', message="Not all required fields were filled correctly")
        else:
            listing = Listings(name = title, description = description, category = category_instance, owner = request.user, price = price, image = image)
            listing.save()
            return render(request, "auctions/index.html", {
                "listings": Listings.objects.all()
            })

def listing(request, listing_id):
    listing = get_object_or_404(Listings, pk = listing_id)
    return render(request, "auctions/listing.html", {
        "listing": listing
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
