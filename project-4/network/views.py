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
    # Redirects the user to the index page
    return redirect('index')


def index(request):
    # Get all posts and order them by timestamp
    all_posts = Post.objects.all().order_by('-timestamp')
    # Paginator to control the number of posts per page
    paginator = Paginator(all_posts, 10)
    # Get the page number from the request
    page_num = request.GET.get('page')
    posts = paginator.get_page(page_num)

    # Handling the post creation on the index page
    if request.method == "POST":
        posting_user = request.user
        post_body = request.POST.get('post-body')
        # Check if the post body is not empty
        if post_body == "":
            # Render the index page with a message if the post body is empty
            return render(request, "network/index.html", {
                "message": "You must type a message in order to post",
                "posts": posts
            })
        else:
            # Create and save the new post if the post body is not empty
            post = Post(user=posting_user, body=post_body)
            post.save()

    # Render the index page with all posts
    return render(request, "network/index.html", {
        "posts": posts
    })


def profile(request, user_id):
    # Get the profile user and their related data
    profile_user = User.objects.get(pk=user_id)
    profile = Profile.objects.get(user=profile_user)
    post_count = Post.objects.filter(user=profile_user).count()
    following_count = Following.objects.filter(user=profile_user).count()
    followers_count = Following.objects.filter(user_followed=profile_user).count()
    user_posts = Post.objects.filter(user=profile_user).order_by('-timestamp')
    # Paginator to control the number of posts per page
    paginator = Paginator(user_posts, 10)
    # Get the page number from the request
    page_num = request.GET.get('page')
    posts = paginator.get_page(page_num)

    if request.user.is_authenticated:
        # Get the list of users that the current user is following
        following_users = Following.objects.filter(user=request.user).values_list('user_followed', flat=True)
        return render(request, "network/profile.html", {
            "profile_user": profile_user,
            "profile": profile,
            "user_posts": posts,
            "post_count": post_count,
            "following_count": following_count,
            "followers_count": followers_count,
            "following_users": following_users
        })
    else:
        # Render the profile page for non-authenticated users without following data
        return render(request, "network/profile.html", {
            "profile_user": profile_user,
            "profile": profile,
            "user_posts": posts,
            "post_count": post_count,
            "following_count": following_count,
            "followers_count": followers_count
        })


def edit_profile(request, user_id):
    # Retrieve the user and their profile based on the user_id
    user = User.objects.get(pk=user_id)
    profile = Profile.objects.get(user=user)

    if request.method == "POST":
        # If the form is submitted, retrieve the updated information
        name = request.POST.get('name')
        bio = request.POST.get('bio')
        profile_picture = request.FILES.get('profile_pic')

        # Update the profile information
        profile.name = name
        profile.bio = bio
        # Update the profile picture if a new one is provided
        if profile_picture:
            profile.picture = profile_picture
        # Save the updated profile
        profile.save()
        # Redirect to the user's profile page after updating
        return redirect('profile', user_id=user_id)

    # Render the edit profile page with the current profile information
    return render(request, "network/edit_profile.html", {
        "user_id": user_id,
        "profile": profile
    })


def following(request):
    # Retrieve the list of users that the current user is following
    users_following = Following.objects.filter(user=request.user)
    following_users = [follow.user_followed for follow in users_following]
    # Get posts from the followed users
    filtered_posts = Post.objects.filter(user__in=following_users).order_by('-timestamp')
    # Paginate the posts
    paginator = Paginator(filtered_posts, 10)
    page_num = request.GET.get('page')
    posts = paginator.get_page(page_num)
    # Render the following page with the posts from followed users
    return render(request, "network/following.html", {
        "posts": posts
    })


def delete_post(request, post_id):
    # Retrieve and delete the specified post
    post = Post.objects.get(pk=post_id)
    post.delete()
    # Redirect to the previous page after deletion
    referer_url = request.META.get('HTTP_REFERER')
    if referer_url:
        return HttpResponseRedirect(referer_url)
    # Redirect to the index page as a fallback if the referer URL is not set
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
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:  # Handle the case where username is already taken
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)  # Log in the newly created user
        return HttpResponseRedirect(reverse("index"))  # Redirect to index page on successful registration
    else:
        # Render the registration page for a GET request
        return render(request, "network/register.html")


def likes(request, post_id):
    # Try to get the post by ID, return an error if not found
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Check if the user is authenticated
    if request.user.is_authenticated:
        if request.method == "POST":
            # Toggle like status: Add a like if the user hasn't liked the post yet, otherwise remove it
            if not request.user in post.liked_by.all():
                post.liked_by.add(request.user)
                post.likes += 1
            else:
                post.liked_by.remove(request.user)
                post.likes -= 1
            post.save()
    
    # Serialize the post data to return as JSON
    serialized_post = {
        'id': post.id,
        'timestamp': post.timestamp,
        'body': post.body,
        'likes': post.likes
    }
    return JsonResponse(serialized_post)


def follow(request, profile_user_id):
    # Get the profile user and the user who made the request
    profile_user = User.objects.get(pk=profile_user_id)
    request_user = request.user
    request_users_following = Following.objects.filter(user=request_user)
    request_following_users = [follow.user_followed for follow in request_users_following]
    
    if request.method == "POST":
        # Toggle follow status: Follow if not following already, otherwise unfollow
        if profile_user not in request_following_users:
            Following.objects.create(user=request_user, user_followed=profile_user)
        else:
            Following.objects.filter(user=request_user, user_followed=profile_user).delete()
    
    # Get updated followers count
    followers_count = Following.objects.filter(user_followed=profile_user).count()
    # Return followers count as JSON
    return JsonResponse({
        'count': followers_count
    })


def edit_post(request, post_id):
    if request.method == "POST":
        # Load data from the request body
        data = json.loads(request.body)
        # Get the post to be edited
        post = Post.objects.get(pk=post_id)
        # Update the post's body
        post.body = data["new_body"]
        post.save()
        # Return the new body of the post as JSON
        return JsonResponse({'new_body': post.body})
