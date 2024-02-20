from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from .models import User, List, Task, Issue
from datetime import datetime
import json

# Create your views here.
def open(request):
    # Redirects the user to the index page
    return redirect('index')


def index(request):
    # Handle form submission for creating a new list
    if request.method == 'POST':
        title = request.POST["title"]  # Get the title of the new list from the form
        new_list = List(owner=request.user, listName=title)  # Create a new list instance
        new_list.save()  # Save the new list to the database
    # Check if the user is authenticated to show them their lists
    if request.user.is_authenticated:
        message = request.session.pop('message', None)  # Retrieve and clear any message from the session
        lists_owned = List.objects.filter(owner=request.user)  # Query for lists owned by the user
        lists_collaborating = List.objects.filter(collaborators=request.user)  # Query for lists where the user is a collaborator
        all_lists = lists_owned.union(lists_collaborating).order_by('order')  # Combine and order the lists
        # Render the index page with context data
        return render(request, "checklist/index.html", {
            "users": User.objects.all(),  # Pass all users for potential list sharing
            "user": request.user,
            "lists": all_lists,
            "message": message
        })
    # If the user is not authenticated, simply render the index page without context data
    return render(request, "checklist/index.html")


def checklist(request, list_id):
    list = List.objects.get(pk=list_id)  # Retrieve the specific list by its primary key
    tasks = Task.objects.filter(list=list)  # Query for tasks that belong to the list
    message = request.session.pop('message', None)  # Retrieve and clear any message from the session
    # Handle form submission for creating a new task
    if request.method == "POST":
        description = request.POST["description"]  # Get the task description from the form
        new_task = Task(list=list, description=description)  # Create a new task instance
        new_task.save()  # Save the new task to the database
        # Redirect back to the checklist page to display the newly added task
        return redirect(reverse('checklist', args=[list_id]))
    # Render the list page with context data for a GET request or the initial page load
    return render(request, "checklist/list.html", {
        "user": request.user,
        "list": list,
        "tasks": tasks,
        "message": message
    })


def issues(request):
    all_unresolved_issues = Issue.objects.filter(timeResolved=None)  # Query for all unresolved issues
    user_related_issues = []
    # Filter issues to include only those related to the user (either owned or collaborated lists)
    for issue in all_unresolved_issues:
        if request.user == issue.task.list.owner or request.user in issue.task.list.collaborators.all():
            user_related_issues.append(issue)
    # Render the issues page with context data
    return render(request, "checklist/issues.html", {
        "issues": user_related_issues
    })


def report_issue(request, task_id):
    # Handles issue reporting for a specific task
    if request.method == 'POST':
        # Create a new Issue object with details from the form
        new_issue = Issue(
            task=Task.objects.get(pk=task_id),  # Link the issue to the specified task
            severity=request.POST.get('severity'),  # Severity level of the issue
            importance=request.POST.get('importance'),  # Importance level of the issue
            description=request.POST.get('description'),  # Description of the issue
            reportedBy=request.user  # User reporting the issue
        )
        new_issue.save()  # Save the new issue to the database
        return redirect('issues')  # Redirect to the issues page


def delete_list(request, list_id):
    # Handles deletion of a specified list
    list = List.objects.get(pk=list_id)  # Retrieve the list by its primary key
    list.delete()  # Delete the list
    return redirect(request.META.get('HTTP_REFERER'))  # Redirect back to the previous page


def leave_list(request, list_id):
    # Allows a user to leave (remove themselves from) a specified list
    list = List.objects.get(pk=list_id)  # Retrieve the list by its primary key
    list.collaborators.remove(request.user)  # Remove the user from the list's collaborators
    return redirect(request.META.get('HTTP_REFERER'))  # Redirect back to the previous page


def edit_list_name(request, list_id):
    # Handles renaming of a specified list
    list = List.objects.get(pk=list_id)  # Retrieve the list by its primary key
    name = request.POST.get('rename_list')  # Get the new name from the form
    list.listName = name  # Update the list's name
    list.save()  # Save the changes to the list
    return redirect(request.META.get('HTTP_REFERER'))  # Redirect back to the previous page


def add_user(request, list_id):
    # Adds a new user as a collaborator to a specified list
    list = List.objects.get(pk=list_id)  # Retrieve the list by its primary key
    user = User.objects.get(pk=request.POST.get('user_id'))  # Retrieve the user to add by their primary key
    if user in list.collaborators.all():
        # Check if the user is already a collaborator and set a message if true
        request.session['message'] = "This user is already a collaborator of the list."
        request.session['message_type'] = "danger"
    else:
        list.collaborators.add(user)  # Add the user as a collaborator
        # Set a success message
        request.session['message'] = "This user is now a collaborator of the list"
        request.session['message_type'] = "success"
    return redirect('index')  # Redirect back to the index page


def remove_user(request, list_id):
    # Retrieves the specified list and user to be removed
    list = List.objects.get(pk=list_id)
    user = User.objects.get(pk=request.POST.get('user_id'))
    # Checks if the user is actually a collaborator of the list
    if user not in list.collaborators.all():
        # Sets a session message indicating the user cannot be removed
        request.session['message'] = "This user isn't removable as they're not a collaborator of the list."
        request.session['message_type'] = "danger"
    else:
        # Removes the user from the list's collaborators
        list.collaborators.remove(user)
        # Sets a success message in the session
        request.session['message'] = "This user is no longer a collaborator of the list"
        request.session['message_type'] = "success"
    return redirect('index')  # Redirects back to the index page


def delete_task(request, task_id):
    # Retrieves and deletes the specified task
    task = Task.objects.get(pk=task_id)
    task.delete()
    return redirect(request.META.get('HTTP_REFERER'))  # Redirects to the previous page


def edit_task(request, task_id):
    # Retrieves the specified task and updates its description
    task = Task.objects.get(pk=task_id)
    description = request.POST.get('edit_task')
    task.description = description
    task.save()
    return redirect(request.META.get('HTTP_REFERER'))  # Redirects to the previous page


def toggle_important(request, task_id):
    # Toggles the important flag of the specified task
    task = Task.objects.get(pk=task_id)
    task.importantFlag = not task.importantFlag  # Flips the boolean value
    task.save()
    return redirect(request.META.get('HTTP_REFERER'))  # Redirects to the previous page


def toggle_issue_status(request, task_id):
    if request.method == 'POST':
        task = Task.objects.get(pk=task_id)
        task.issueStatus = not task.issueStatus  # Flips the issue status
        # If the task now has an issue, record the user and timestamp
        if task.issueStatus:
            task.alertedBy = request.user
            task.timeAlertedIssue = datetime.now()
        else:
            # Resets the issue reporting fields if the issue is cleared
            task.alertedBy = None
            task.timeAlertedIssue = None
        task.save()
        # Returns a JSON response indicating success and the current completed status
        return JsonResponse({'success': True, 'completedStatus': task.completedStatus})


def toggle_completion_status(request, task_id):
    if request.method == 'POST':
        task = Task.objects.get(pk=task_id)
        task.completedStatus = not task.completedStatus  # Flips the completion status
        # If the task is now marked as completed, record the user and timestamp
        if task.completedStatus:
            task.completedBy = request.user
            task.timeCompleted = datetime.now()
        else:
            # Resets the completion fields if the task is marked as incomplete
            task.completedBy = None
            task.timeCompleted = None
        task.save()
        # Returns a JSON response indicating success and the current issue status
        return JsonResponse({'success': True, 'issueStatus': task.issueStatus})
    

def resolve_issue(request, issue_id):
    # Handles the resolution of a specified issue
    if request.method == 'POST':
        issue = Issue.objects.get(pk=issue_id)  # Retrieve the issue by its ID
        issue.timeResolved = datetime.now()  # Set the resolution time to now
        issue.save()  # Save the updated issue
        return JsonResponse({'success': True})  # Return a success response


def delete_issue(request, issue_id):
    # Deletes a specified issue
    if request.method == 'POST':
        issue = Issue.objects.get(pk=issue_id)  # Retrieve the issue by its ID
        issue.delete()  # Delete the issue
        return JsonResponse({'success': True})  # Return a success response


def clear_tasks(request, list_id):
    # Clears (resets) all tasks within a specified list
    if request.method == 'POST':
        tasks = Task.objects.filter(list=list_id)  # Retrieve all tasks for the specified list
        for task in tasks:
            # Reset attributes for each task
            task.completedStatus = False
            task.completedBy = None
            task.timeCompleted = None
            task.issueStatus = False
            task.alertedBy = None
            task.timeAlertedIssue = None
            task.save()  # Save the updated task
        # Set a success message in the session
        request.session['message'] = "All tasks have been cleared."
        request.session['message_type'] = "success"
        return JsonResponse({'success': True})  # Return a success response


def clear_lists(request):
    # Clears (resets) all tasks across all lists
    if request.method == 'POST':
        tasks = Task.objects.all()  # Retrieve all tasks
        for task in tasks:
            # Reset attributes for each task
            task.completedStatus = False
            task.completedBy = None
            task.timeCompleted = None
            task.issueStatus = False
            task.alertedBy = None
            task.timeAlertedIssue = None
            task.save()  # Save the updated task
        # Set a success message in the session
        request.session['message'] = "Tasks in all lists have been cleared."
        request.session['message_type'] = "success"
        return JsonResponse({'success': True})  # Return a success response


def history(request):
    # Retrieves and displays the history of resolved issues related to the user
    message = request.session.pop('message', None)  # Retrieve and clear any message from the session
    all_resolved_issues = Issue.objects.exclude(timeResolved=None)  # Retrieve all resolved issues
    user_related_issues = []
    # Filter issues related to the user either as an owner or collaborator
    for issue in all_resolved_issues:
        if request.user == issue.task.list.owner or request.user in issue.task.list.collaborators.all():
            user_related_issues.append(issue)
    # Render the history page with context data
    return render(request, "checklist/history.html", {
        "issues": user_related_issues,
        "message": message
    })


def update_order(request):
    # Updates the order of tasks or lists based on user interaction
    data = json.loads(request.body)  # Parse the JSON body to a Python dictionary
    order_type = data.get('type')  # Determine whether updating 'task' or 'list'
    order_ids = data.get('order', [])  # Get the new order of IDs
    if order_type == 'task':
        # Update each task with its new order
        for index, id in enumerate(order_ids, start=1):
            Task.objects.filter(id=id).update(order=index)
    elif order_type == 'list':
        # Update each list with its new order
        for index, id in enumerate(order_ids, start=1):
            List.objects.filter(id=id).update(order=index)
    return JsonResponse({"status": "success"})  # Return a success status


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication was successful
        if user is not None:
            login(request, user)
            request.session['message'] = "You are now logged in."
            request.session['message_type'] = "success"
            return HttpResponseRedirect(reverse("index"))  # Redirect to index page on successful login
        else:
            return render(request, "checklist/login.html", {
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
