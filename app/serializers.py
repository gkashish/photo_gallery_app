from rest_framework import serializers
from rest_framework.response import Response

from .models import Profile, Photo, Album, LikePhoto, LikeAlbum
from django.contrib.auth.models import User
from django.http.response import *


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("user", "profile_picture", "gender")

    def create(self, validated_data):
        try:
            us = User.objects.create(
                username=validated_data['username'],
                first_name=validated_data['firstName'],
                last_name=validated_data['lastName']
            )
        except:
            return HttpResponseBadRequest("Username already exists.")
        us.set_password(validated_data['password'])
        us.save()
        profile = Profile.objects.get(user__username=us.username)
        profile.gender = validated_data['gender']
        if validated_data['profilePic'] is not None:
            profile.profile_picture = validated_data['profilePic']
        profile.save()
        return Response("Success!")


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ("name", "description", "privacy", "user", "album", "created_at")


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ("name", "description", "cover_photo", "privacy", "user", "created_at", "likes", "liked")

class LikePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikePhoto
        fields = ("user", "liked_to")


class LikeAlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeAlbum
        fields = ("user", "liked_to")
