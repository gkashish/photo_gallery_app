from rest_framework import serializers
from .models import Owner, Photo, Album, Likes


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ("username", "name")


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ("name", "description", "privacy", "username", "album", "created_on")


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ("name", "description", "cover_photo", "privacy", "username", "created_on")


class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = ("username", "album", "song", "liked_by")
