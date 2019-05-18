from rest_framework import serializers
from .models import Profile, Photo, Album, LikePhoto, LikeAlbum


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("user", "profile_picture", "gender")


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ("name", "description", "privacy", "user", "album", "created_at")


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ("name", "description", "cover_photo", "privacy", "user", "created_at")


class LikePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikePhoto
        fields = ("user", "liked_to")


class LikeAlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeAlbum
        fields = ("user", "liked_to")
