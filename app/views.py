from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Owner, Album, Likes, Photo
from .serializers import OwnerSerializer, AlbumSerializer, LikesSerializer, PhotoSerializer


class ListAlbumView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    serializer_class = AlbumSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        print(user)
        return Album.objects.filter(name=user)
