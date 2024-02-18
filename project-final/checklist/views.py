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
    if request.method == 'POST':
        title = request.POST["title"]
        new_list = List(owner=request.user, listName=title)
        new_list.save()
    if request.user.is_authenticated:
        message = request.session.pop('message', None)
        lists_owned = List.objects.filter(owner=request.user)
        lists_collaborating = List.objects.filter(collaborators=request.user)
        all_lists = lists_owned.union(lists_collaborating).order_by('order')
        return render(request, "checklist/index.html", {
            "users": User.objects.all(),
            "user": request.user,
            "lists": all_lists,
            "message": message
        })
    return render(request, "checklist/index.html")


def checklist(request, list_id):
    list = List.objects.get(pk=list_id)
    tasks = Task.objects.filter(list=list)
    message = request.session.pop('message', None)
    if request.method == "POST":
        description = request.POST["description"]
        new_task = Task(list=list, description=description)
        new_task.save()
        # Redirect to the same page with a GET request
        return redirect(reverse('checklist', args=[list_id]))
    # For a GET request, or the initial load
    return render(request, "checklist/list.html", {
        "user": request.user,
        "list": list,
        "tasks": tasks,
        "message": message
    })


def issues(request):
    all_unresolved_issues = Issue.objects.filter(timeResolved=None)
    user_related_issues = []
    for issue in all_unresolved_issues:
        if request.user == issue.task.list.owner or request.user in issue.task.list.collaborators.all():
            user_related_issues.append(issue)
    return render(request, "checklist/issues.html", {
        "issues": user_related_issues
    })


def report_issue(request, task_id):
    if request.method == 'POST':
        new_issue = Issue(
            task=Task.objects.get(pk=task_id),
            severity=request.POST.get('severity'),
            importance=request.POST.get('importance'),
            description=request.POST.get('description'),
            reportedBy=request.user
        )
        new_issue.save()
        return redirect('issues')


def delete_list(request, list_id):
    # Retrieve and delete the specified list
    list = List.objects.get(pk=list_id)
    list.delete()
    return redirect(request.META.get('HTTP_REFERER'))


def leave_list(request, list_id):
    # Retrieve and remove the user from the specified list
    list = List.objects.get(pk=list_id)
    list.collaborators.remove(request.user)
    return redirect(request.META.get('HTTP_REFERER'))


def edit_list_name(request, list_id):
    # Retrieve the list and edit the name
    list = List.objects.get(pk=list_id)
    name = request.POST.get('rename_list')
    list.listName = name
    list.save()
    return redirect(request.META.get('HTTP_REFERER'))


def add_user(request, list_id):
    # Retrieve the list and add the user
    list = List.objects.get(pk=list_id)
    user = User.objects.get(pk=request.POST.get('user_id'))
    if user in list.collaborators.all():
        request.session['message'] = "This user is already a collaborator of the list."
        request.session['message_type'] = "danger"
        return redirect('index')
    list.collaborators.add(user)
    request.session['message'] = "This user is now a collaborator of the list"
    request.session['message_type'] = "success"
    return redirect('index')


def remove_user(request, list_id):
    # Retrieve the list and add the user
    list = List.objects.get(pk=list_id)
    user = User.objects.get(pk=request.POST.get('user_id'))
    if user not in list.collaborators.all():
        request.session['message'] = "This user isn't removable as they're not a collaborator of the list."
        request.session['message_type'] = "danger"
        return redirect('index')
    list.collaborators.remove(user)
    request.session['message'] = "This user is no longer a collaborator of the list"
    request.session['message_type'] = "success"
    return redirect('index')


def delete_task(request, task_id):
    # Retrieve and delete the specified task
    task = Task.objects.get(pk=task_id)
    task.delete()
    return redirect(request.META.get('HTTP_REFERER'))


def edit_task(request, task_id):
    # Retrieve the list and edit the name
    task = Task.objects.get(pk=task_id)
    description = request.POST.get('edit_task')
    task.description = description
    task.save()
    return redirect(request.META.get('HTTP_REFERER'))


def toggle_important(request, task_id):
    task = Task.objects.get(pk=task_id)
    task.importantFlag = not task.importantFlag
    task.save()
    return redirect(request.META.get('HTTP_REFERER'))


def toggle_issue_status(request, task_id):
    if request.method == 'POST':
        task = Task.objects.get(pk=task_id)
        task.issueStatus = not task.issueStatus
        if task.issueStatus == True:
            task.alertedBy = request.user
            task.timeAlertedIssue = datetime.now()
        else:
            task.alertedBy = None
            task.timeAlertedIssue = None
        task.save()
        return JsonResponse({'success': True, 'completedStatus': '{{ task.completedStatus }}'})


def toggle_completion_status(request, task_id):
    if request.method == 'POST':
        task = Task.objects.get(pk=task_id)
        task.completedStatus = not task.completedStatus
        if task.completedStatus == True:
            task.completedBy = request.user
            task.timeCompleted = datetime.now()
        else:
            task.completedBy = None
            task.timeCompleted = None
        task.save()
        return JsonResponse({'success': True, 'issueStatus': '{{ task.issueStatus }}'})
    

def resolve_issue(request, issue_id):
    if request.method == 'POST':
        issue = Issue.objects.get(pk=issue_id)
        issue.timeResolved = datetime.now()
        issue.save()
        return JsonResponse({'success': True})
    

def delete_issue(request, issue_id):
    print("reached here")
    if request.method == 'POST':
        issue = Issue.objects.get(pk=issue_id)
        issue.delete()
        return JsonResponse({'success': True})
    

def clear_tasks(request, list_id):
    if request.method == 'POST':
        tasks = Task.objects.filter(list=list_id)
        for task in tasks:
            task.completedStatus = False
            task.completedBy = None
            task.timeCompleted = None
            task.issueStatus = False
            task.alertedBy = None
            task.timeAlertedIssue = None
            task.save()
        request.session['message'] = "All tasks have been cleared."
        request.session['message_type'] = "success"
        return JsonResponse({'success': True})
    

def clear_lists(request):
    if request.method == 'POST':
        tasks = Task.objects.all()
        for task in tasks:
            task.completedStatus = False
            task.completedBy = None
            task.timeCompleted = None
            task.issueStatus = False
            task.alertedBy = None
            task.timeAlertedIssue = None
            task.save()
        request.session['message'] = "Tasks in all lists have been cleared."
        request.session['message_type'] = "success"
        return JsonResponse({'success': True})


def history(request):
    message = request.session.pop('message', None)
    all_resolved_issues = Issue.objects.exclude(timeResolved=None)
    user_related_issues = []
    for issue in all_resolved_issues:
        if request.user == issue.task.list.owner or request.user in issue.task.list.collaborators.all():
            user_related_issues.append(issue)
    return render(request, "checklist/history.html", {
        "issues": user_related_issues,
        "message": message
    })


def update_order(request):
    # Load JSON string from request.body and convert it to Python dict
    data = json.loads(request.body)
    order_type = data.get('type')  # Get the type ('task' or 'list')
    order_ids = data.get('order', [])
    if order_type == 'task':
        for index, id in enumerate(order_ids, start=1):
            Task.objects.filter(id=id).update(order=index)
    elif order_type == 'list':
        for index, id in enumerate(order_ids, start=1):
            List.objects.filter(id=id).update(order=index)
    return JsonResponse({"status": "success"})


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
