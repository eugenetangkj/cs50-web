from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from . import util
from markdown2 import Markdown
import random



### Form Classes

## A search entry form
class NewSearchForm(forms.Form):
    search_entry = forms.CharField(label="Search Encyclopedia")

## A new entry form for title
class NewAddTitleForm(forms.Form):
    title_field = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control col-md-2 col-lg-2', 'rows':1}),
                                 label="Enter Page Title")

## A new entry form for body
class NewAddBodyForm(forms.Form):
    body_field = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control col-md-8 col-lg-8', 'rows':5}),
                                 label="Enter Page Content")


### View Functions

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewSearchForm()
    })

def entry(request, entry_name):
        # Gets the HTML content
        html_content = get_html_content(entry_name)

        # Render the webpage by substituting the correct values into the entry template
        return render(request, "encyclopedia/entry.html", {
              "entry_name": entry_name,
              "entry_body": html_content,
              "form": NewSearchForm()
        })

def search(request):
    # Came to this page via a POST request
    if request.method == "POST":

        # Take in the data that the user submitted
        form = NewSearchForm(request.POST)

        # Check if form data is valid via server-side authentication
        if form.is_valid():

            # Isolate the search term from the cleaned version of the form data
            search_term = form.cleaned_data["search_entry"]
            
            # Entry exists
            if (does_entry_exist(search_term)):
                return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={"entry_name": search_term}))
                   
            # Entry does not exist
            else:
                return render(request, "encyclopedia/search.html", {
                "results": get_substring_entries(util.list_entries(), search_term),
                "form": NewSearchForm(),
            })
    
    # Came to this page via a GET request
    return render(request, "encyclopedia/search.html", {
        "results": [],
        "form": NewSearchForm()
        })       

def add(request):
    # Came to this page via a POST request
    if request.method == "POST":

        # Take in the data that the user submitted
        form_title = NewAddTitleForm(request.POST)
        form_body = NewAddBodyForm(request.POST)



        # Check if form data is valid via server-side authentication
        if (form_title.is_valid() and form_body.is_valid()):

            # Isolate the values from the cleaned version of the form data
            title = form_title.cleaned_data["title_field"]
            body = form_body.cleaned_data["body_field"]

            # Entry already exists
            if (does_entry_exist(title)):
                # Display error message
                return render(request, "encyclopedia/add.html", {
                "form": NewSearchForm(),
                "add_form_title": NewAddTitleForm(),
                "add_form_body": NewAddBodyForm(),
                "error": 1,
                "page_title": title
            })

  
            # Entry does not exist
            else:
                util.save_entry(title, bytes(body, 'utf8'))
                return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={"entry_name": title}))

    
    # Came to this page via a GET request
    return render(request, "encyclopedia/add.html", {
        "form": NewSearchForm(),
        "add_form_title": NewAddTitleForm(),
        "add_form_body": NewAddBodyForm(),
        "error": 0,
        "page_title": ""
    })


def edit(request, entry_name):
    # Came to this page via a POST request
    if request.method == "POST":

        # Take in the data that the user submitted
        form_body = NewAddBodyForm(request.POST)

        # Check if form data is valid via server-side authentication
        if (form_body.is_valid()):

            # Isolate the values from the cleaned version of the form data
            body = form_body.cleaned_data["body_field"]

            ## Save file to disk and redirect accordingly
            util.save_entry(entry_name, bytes(body, 'utf8'))
            return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={"entry_name": entry_name}))




    # Came to this page via a GET request
    form_body = NewAddBodyForm({"body_field": util.get_entry(entry_name)})
    return render(request, "encyclopedia/edit.html", {
        "form": NewSearchForm(),
        "page_title": entry_name,
        "add_form_body": form_body
    })

def randomise(request):
    list_of_entries = util.list_entries()
    chosen_title = random.choice(list_of_entries)
    return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={"entry_name":chosen_title}))


### Helper Functions

## Gets the HTML content from an entry if its Markdown file exists, else return None.
def get_html_content(entry_name):
     # Gets the Markdown content
    markdown_content = util.get_entry(entry_name)

    html_content = None

    # Check whether Markdown entry exists or not
    if (markdown_content is not None):
        # Convert Markdown into HTML
        html_content = Markdown().convert(markdown_content)
    return html_content

## Checks if search_term is a valid entry or not
def does_entry_exist(search_term):
    if util.get_entry(search_term) is None:
        return False
    return True

## Gets the entries that contain search_term as a substring
def get_substring_entries(list_of_entries, search_term):
    list_of_substring_entries = []
    for entry in list_of_entries:
        if search_term in entry:
            list_of_substring_entries.append(entry)
    return list_of_substring_entries
    





