from django.urls import path

from . import views

app_name = 'encyclopedia'
urlpatterns = [
    path("wiki", views.index, name="index"),
    path("wiki/<str:entry_name>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("add", views.add, name="add"),
    path("edit/<str:entry_name>", views.edit, name="edit"),
    path("random", views.randomise, name="random")
]
