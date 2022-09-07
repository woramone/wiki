from xml.etree.ElementInclude import include
from django.urls import path

from . import views



urlpatterns = [
    path("", views.index, name="index"),
    path("random", views.random_page, name="random"),
    path("search", views.search, name="search"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("newpage", views.newpage, name="newpage"),
    path("edit/<str:title>",views.edit, name="edit"),
    
    
]
