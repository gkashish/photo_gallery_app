from rest_framework import serializers
from rest_framework.response import Response

from .models import Profile, Photo, Album, LikePhoto, LikeAlbum
from django.contrib.auth.models import User
from django.http.response import *

def upload_pic_to_firebase(file, name):
    from google.cloud import storage
    # client = storage.Client()
    # https://console.cloud.google.com/storage/browser/[bucket-id]/
    storage_client = storage.Client.from_service_account_json(
        './photo-gallery-app-ad880f831cbf.json')
    bucket = storage_client.get_bucket('photo-gallery-app-e79f8.appspot.com')
    # Then do other things...
    # blob = bucket.get_blob('remote/path/to/file.txt')
    # print(blob.download_as_string())
    # blob.upload_from_string('New contents!')
    blob2 = bucket.blob(name)
    blob2.upload_from_file(file)




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
        upload_pic_to_firebase(profile.profile_picture.file, profile.profile_picture.name)
        return Response("Success!")


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ("name", "description", "privacy", "user", "album", "created_at")

    def create(self, validated_data):
        photo = Photo.objects.create(
            file=validated_data['picture'],
            description=validated_data['description'],
            privacy=validated_data['privacy'],
            user_id=validated_data['user'],
            album_id=validated_data['album']
        )

        upload_pic_to_firebase(photo.file.file, photo.file.name)
        return Response("Success!")


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ("name", "description", "cover_photo", "privacy", "user", "created_at")

    def create(self, validated_data):
        album = Album.objects.create(
            name=validated_data['albumName'],
            privacy=validated_data['privacy'],
            cover_photo=validated_data['coverPic'],
            description=validated_data['description'],
            user_id=validated_data['user']
        )
        upload_pic_to_firebase(album.cover_photo.file, album.cover_photo.name)
        return Response("Success!")


class LikePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikePhoto
        fields = ("user", "liked_to")


class LikeAlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeAlbum
        fields = ("user", "liked_to")
