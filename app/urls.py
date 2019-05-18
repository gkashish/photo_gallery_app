from django.urls import path
from . import views

urlpatterns = [
    path('myalbums/', views.my_albums, name="user_albums"),
    path('albums/', views.all_albums, name="all_albums"),
    path('newalbum/', views.all_albums, name="all_albums"),
]
