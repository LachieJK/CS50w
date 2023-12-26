from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse
from .models import User, Profile, Following, Post, Comment
from django.views.decorators.csrf import csrf_exempt

def index(request):
    if request.method == "POST":
        posting_user = request.user 
        post_body = request.POST.get('post-body')
        post = Post(user=posting_user, body=post_body)
        post.save()
        return render(request, "network/index.html", {
            "posts": Post.objects.all().order_by('-timestamp')
        })
    else: 
        return render(request, "network/index.html", {
            "posts": Post.objects.all().order_by('-timestamp')
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@csrf_exempt
def likes(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.user.is_authenticated:
        if request.method == "POST":
            if not request.user in post.liked_by.all():
                post.liked_by.add(request.user)
                post.likes += 1
            else:
                post.liked_by.remove(request.user)
                post.likes -= 1
            post.save()
 
    serialized_post = {
        'id': post.id,
        'timestamp': post.timestamp,
        'body': post.body,
        'likes': post.likes
    }
    return JsonResponse(serialized_post)