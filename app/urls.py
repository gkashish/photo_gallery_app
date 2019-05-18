from django.urls import path
from .views import ListAlbumView


urlpatterns = [
    path('songs/', ListAlbumView.as_view(), name="albums_user")
]