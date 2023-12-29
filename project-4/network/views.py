from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from .models import User, Profile, Following, Post
from django.core.paginator import Paginator
import json

def open(request):
    return redirect('index');

def index(request):
    all_posts = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(all_posts, 10)
    page_num = request.GET.get('page')
    posts = paginator.get_page(page_num)

    if request.method == "POST":
        posting_user = request.user 
        post_body = request.POST.get('post-body')
        if post_body == "":
            return render(request, "network/index.html", {
                "message": "You must type a message in order to post",
                "posts": posts
            })
        else:
            post = Post(user=posting_user, body=post_body)
            post.save()

    return render(request, "network/index.html", {
        "posts": posts
    })


def profile(request, user_id):
    if request.user.is_authenticated:
        profile_user = User.objects.get(pk=user_id)
        profile = Profile.objects.get(user=profile_user)
        user_posts = Post.objects.filter(user=profile_user).order_by('-timestamp')
        post_count = Post.objects.filter(user=profile_user).count()
        following_count = Following.objects.filter(user=profile_user).count()
        followers_count = Following.objects.filter(user_followed=profile_user).count()
        following_users = Following.objects.filter(user=request.user).values_list('user_followed', flat=True)
        return render(request, "network/profile.html", {
            "profile_user": profile_user,
            "profile": profile,
            "user_posts": user_posts,
            "post_count": post_count,
            "following_count": following_count,
            "followers_count": followers_count,
            "following_users": following_users
        })
    else:
        profile_user = User.objects.get(pk=user_id)
        profile = Profile.objects.get(user=profile_user)
        user_posts = Post.objects.filter(user=profile_user).order_by('-timestamp')
        post_count = Post.objects.filter(user=profile_user).count()
        following_count = Following.objects.filter(user=profile_user).count()
        followers_count = Following.objects.filter(user_followed=profile_user).count()
        return render(request, "network/profile.html", {
            "profile_user": profile_user,
            "profile": profile,
            "user_posts": user_posts,
            "post_count": post_count,
            "following_count": following_count,
            "followers_count": followers_count
        })
    

def edit_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    profile = Profile.objects.get(user=user)
    if request.method == "GET":
        return render(request, "network/edit_profile.html", {
            "user_id": user_id,
            "profile": profile
        })
    else:
        name = request.POST.get('name')
        bio = request.POST.get('bio')
        profile_picture = request.FILES.get('profile_pic')
        profile.name = name
        profile.bio = bio
        if profile_picture:
            profile.picture = profile_picture
        profile.save()
        return redirect('profile', user_id=user_id)


def following(request):
    users_following = Following.objects.filter(user=request.user)
    following_users = [follow.user_followed for follow in users_following]
    filtered_posts = Post.objects.filter(user__in=following_users).order_by('-timestamp')
    paginator = Paginator(filtered_posts, 10)
    page_num = request.GET.get('page')
    posts = paginator.get_page(page_num)
    return render(request, "network/following.html", {
        "posts": posts
    })


def delete_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.delete()
    referer_url = request.META.get('HTTP_REFERER')
    if referer_url:
        return HttpResponseRedirect(referer_url)
    # Fallback if referer URL is not set
    return HttpResponseRedirect('/index')


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


def follow(request, profile_user_id):
    profile_user = User.objects.get(pk=profile_user_id)
    request_user = request.user
    request_users_following = Following.objects.filter(user=request_user)
    request_following_users = [follow.user_followed for follow in request_users_following]
    
    if request.method == "POST":
        if profile_user not in request_following_users:
            Following.objects.create(user=request_user, user_followed=profile_user)
        else:
             Following.objects.filter(user=request_user, user_followed=profile_user).delete()
    
    followers_count = Following.objects.filter(user_followed=profile_user).count()
    return JsonResponse({
        'count': followers_count
    })


def edit_post(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        post = Post.objects.get(pk=post_id)
        post.body = data["new_body"]
        post.save()
        return JsonResponse({'new_body': post.body})