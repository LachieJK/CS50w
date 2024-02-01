from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from .models import User, List, Task
from itertools import chain

# Create your views here.
def open(request):
    # Redirects the user to the index page
    return redirect('index')


def index(request):
    if request.method == 'POST':
        title = request.POST["title"]
        new_list = List(owner=request.user, listName=title)
        new_list.save()
    lists_owned = List.objects.filter(owner=request.user)
    lists_collaborating = List.objects.filter(collaborators=request.user)
    all_lists = list(chain(lists_owned, lists_collaborating))
    return render(request, "checklist/index.html", {
        "user": request.user,
        "lists": all_lists
    })


def delete_list(request, list_id):
    # Retrieve and delete the specified list
    list = List.objects.get(pk=list_id)
    list.delete()
    return HttpResponseRedirect('/index')


def edit_list_name(request, list_id):
    # Retrieve the list and edit the name
    list = List.objects.get(pk=list_id)
    name = request.POST.get('rename_list')
    print(name)
    list.listName = name
    list.save()
    return HttpResponseRedirect('/index')


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication was successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))  # Redirect to index page on successful login
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        # Render the login page for a GET request
        return render(request, "checklist/login.html")


def logout_view(request):
    # Logout the user
    logout(request)
    return HttpResponseRedirect(reverse("index"))  # Redirect to index page after logout


def register(request):
    if request.method == "POST":
        # Get user credentials from POST request
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "checklist/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:  # Handle the case where username is already taken
            return render(request, "checklist/register.html", {
                "message": "Username already taken."
            })
        login(request, user)  # Log in the newly created user
        return HttpResponseRedirect(reverse("index"))  # Redirect to index page on successful registration
    else:
        # Render the registration page for a GET request
        return render(request, "checklist/register.html")
