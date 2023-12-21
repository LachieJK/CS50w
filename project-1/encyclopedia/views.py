from django.shortcuts import render, redirect
import random
from markdown2 import Markdown
from . import util

def converter(title):
    entry = util.get_entry(title)
    markdowner = Markdown()
    if entry is None:
        return None
    else:
        return markdowner.convert(entry)

def entry(request, title):
    content = converter(title)
    if content is None:
        return render(request, "encyclopedia/notFound.html")
    else:
        return render(request, "encyclopedia/entry.html", {
                      "title": title,
                      "content": content})
    
def search(request):
    if request.method == "POST":
        term = request.POST.get('q')
        if term:
            content = converter(term)
            if content is not None:
                return render(request, "encyclopedia/entry.html", {
                        "content": content})
            else:
                entries = util.list_entries()
                similar = []
                for entry in entries:
                    if term.lower() in entry.lower():
                        similar.append(entry)
                return render(request, "encyclopedia/index.html", {
                    "entries": similar
                })

def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html")
    else:
        title = request.POST.get('title');
        content = request.POST.get('content');
        titleExists = util.get_entry(title)
        if titleExists is not None:
            return render(request, "encyclopedia/alreadyExists.html")
        else:
            util.save_entry(title, content)
            formattedContent = converter(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": formattedContent
            })

def edit(request):
    if request.method == "POST":
        title = request.POST.get('title');
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })
    
def save(request):
    if request.method == "POST":
        title = request.POST.get('title');
        content = request.POST.get('content');
        util.save_entry(title, content)
        formattedContent = converter(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": formattedContent
        })

def random_page(request):
    all = util.list_entries()
    randomPage = random.choice(all)
    return redirect('entry', title=randomPage)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

