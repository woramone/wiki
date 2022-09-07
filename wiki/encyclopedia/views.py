from email import message
from re import template
from unittest import result
from django.shortcuts import render
import markdown2
from django.http import HttpResponse
from django import forms
import random
from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

#  Render a page that displays the contents of that encyclopedia entry
def entry(request, title):
    entry_html = markdown2.markdown(util.get_entry(title))
    if entry_html == None:
        return HttpResponse("Your requested page was not found.")
        
    return render(request, "encyclopedia/entry.html", {
         "entry": entry_html, 
         "title": title  
        })

# Search for an encyclopedia entry
def search(request):
    
    query = request.GET.get('q', '')
    entries = util.list_entries()

    try:
        entry_html = markdown2.markdown(util.get_entry(query))
        return render(request, "encyclopedia/entry.html", {
        "entry": entry_html,
        "title": query
        })
    except:
        results = [entry for entry in entries if query.lower() in entry.lower()]
        return render(request, "encyclopedia/search.html", {
            "entries": results
            })

# Create a new encyclopedia entry
def newpage(request):
    if request.method == "POST":   
        title = request.POST.get("title").upper()
        content = request.POST.get("content")
        entries = util.list_entries()
        # If the entry is not yet exist    
        if title not in entries: 
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "entry": content
            })    
        else:
            # Already exists
            return HttpResponse("This entry already exists.")
        
    else:
        return render(request, "encyclopedia/newpage.html")

class EntryForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea, initial="content")
    def __str__(self):
        return self.title
           
# Edit entry’s Markdown content    
def edit(request, title):
    entry = util.get_entry(title)
    if request.method == "GET":   
        return render(request, "encyclopedia/edit.html", { 
            "form": EntryForm(initial={"content": entry, "title": title}),
        })
    else:
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry.html", { 
            "title": title,
            "entry": content
            })
# Random encyclopedia entry   
def random_page(request):
    entries = util.list_entries()
    random_page = random.choice(entries)
    return render(request, "encyclopedia/random_page.html", {
        "entry": random_page
    })