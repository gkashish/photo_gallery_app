import base64
import json

import requests
from PIL import Image
from django.contrib.auth.hashers import check_password
from django.core import serializers
from django.core.files.base import ContentFile
from django.http.response import *
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser

from .models import Profile, Album, Photo, LikeAlbum, LikePhoto
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from .serializers import AlbumSerializer, PhotoSerializer, ProfileSerializer
from django.db.models import Q
from rest_framework.authtoken.models import Token


# def re(request):
#     return redirect("/home/")


class PublicAlbums(APIView):
    def get(self, request):
        # albums=Album.objects.filter(user=request.user)
        albums = Album.objects.filter(Q(user=request.user) | Q(privacy='public'))
        serializer = AlbumSerializer(albums, many=True)
        return Response({"albums": serializer.data})


class AlbumsAPIView(APIView):
    parser_class = (FileUploadParser,)

    def get(self, request):
        # albums=Album.objects.filter(user=request.user)
        albums = Album.objects.filter(Q(user=request.user) | Q(privacy='public'))
        serializer = AlbumSerializer(albums, many=True)
        return Response({"albums": serializer.data})

    def post(self, request):
        data = request.data.copy()
        print(data)
        data['user'] = request.user.pk
        album_serializer = AlbumSerializer(data=data)
        if album_serializer.is_valid():
            album_serializer.save()
            return Response(album_serializer.data, status=status.HTTP_201_CREATED)
        return Response(album_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LikeAPIView(APIView):
    def post(self, request):
        if (request.data.get('type', None) == None or request.data.get('id', None) == None):
            return Response({"error": "Data is missing"}, status=status.HTTP_400_BAD_REQUEST)
        obj_id = request.data.get('id', None)
        if (request.data.get('type', None) == 'album'):
            try:
                album = Album.objects.get(pk=obj_id)
            except Album.DoesNotExist:
                return Response({"error": "Album id is wrong"}, status=status.HTTP_400_BAD_REQUEST)
            is_liked = LikeAlbum.objects.filter(user=request.user.pk, liked_to=obj_id).count()
            if (is_liked):
                obj = LikeAlbum.objects.get(user=request.user, liked_to=album)
                obj.delete()
                c = LikeAlbum.objects.filter(liked_to=obj_id).count()
                return Response({"likes": c, "liked": False})
            else:
                obj = LikeAlbum.objects.create(user=request.user, liked_to=album)
                obj.save()
                c = LikeAlbum.objects.filter(liked_to=obj_id).count()
                return Response({"likes": c, "liked": True})
        if (request.data.get('type', None) == 'photo'):
            try:
                photo = Photo.objects.get(pk=obj_id)
            except Photo.DoesNotExist:
                return Response({"error": "Photo id is wrong"}, status=status.HTTP_400_BAD_REQUEST)
            is_liked = LikePhoto.objects.filter(user=request.user.pk, liked_to=obj_id).count()
            if (is_liked):
                obj = LikePhoto.objects.get(user=request.user, liked_to=obj_id)
                obj.delete()
                c = LikePhoto.objects.filter(liked_to=obj_id).count()
                return Response({"likes": c, "liked": False})
            else:
                obj = LikePhoto.objects.create(user=request.user, liked_to=obj_id)
                obj.save()
                c = LikePhoto.objects.filter(liked_to=obj_id).count()
                return Response({"likes": c, "liked": True})
        return Response({"error": "type is wrong!!"}, status=status.HTTP_400_BAD_REQUEST)


class PhotosAPIView(APIView):
    def get(self, request, pk, format=None):
        photos = Photo.objects.filter(Q(album=pk) & (Q(user=request.user) | Q(privacy='public')))
        serializer = PhotoSerializer(photos, many=True)
        return Response({"photos": serializer.data}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def photo(request, name):
    print(name)
    # response = HttpResponse(mimetype="image/png")
    obj = Album.objects.get(cover_photo="photos/" + name)
    # obj.cover_photo.file
    # img = Image.open('photos/'+name)
    # img.save(response, 'png')
    return HttpResponse(obj.cover_photo.file, content_type="image/*")


class AddPhotoAPIView(APIView):
    parser_class = (FileUploadParser,)

    def get_object(self, pk):
        try:
            return Album.objects.get(pk=pk)
        except Album.DoesNotExist:
            raise Http404

    def post(self, request, pk, format=None):
        data = request.data
        data['user'] = request.user.pk
        data['album'] = pk
        serializer = PhotoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PhotoDetailView(APIView):
    parser_class = (FileUploadParser,)

    def get_object(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise Http404

    def get_Albumobject(self, pk):
        try:
            return Album.objects.get(pk=pk)
        except Album.DoesNotExist:
            raise Http404

    def get(self, request, pk, album, format=None):
        photo = self.get_object(pk)
        serializer = PhotoSerializer(photo)
        return Response(serializer.data)

    def delete(self, request, pk, album, format=None):
        photo = self.get_object(pk)
        photo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AlbumDetailView(APIView):
    parser_class = (FileUploadParser,)

    def get_object(self, pk):
        try:
            return Album.objects.get(pk=pk)
        except Album.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        album = self.get_object(pk)
        serializer = AlbumSerializer(album)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        album = self.get_object(pk)
        data = request.data
        data['user'] = "1"
        serializer = AlbumSerializer(album, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        album = self.get_object(pk)
        album.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@login_required(login_url='/login/')
def my_albums(request):
    if request.method == "GET":
        if request.user.username:
            if User.objects.filter(username=request.user.username).exists():
                user = User.objects.get(username=request.user.username)
            else:
                return HttpResponse("No user exist with this username.")
        else:
            return HttpResponse("No user exist with this username.")

        albums = Album.objects.filter(user=user)
        likes, liked = [], []
        for i in albums:
            likes.append(len(LikeAlbum.objects.filter(liked_to=i)))
            if LikeAlbum.objects.filter(liked_to=i).filter(user=request.user):
                liked.append(True)
            else:
                liked.append(False)

        data = {"Albums": serializers.serialize(queryset=albums, format="xml"), "liked": liked, "likes": likes}
        print(data)
        return JsonResponse(data)
    if request.method == "POST":
        like(request)


from rest_framework import serializers


class Ser(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ("name", "description", "id", "liked", "created_at", "likes")


@api_view(['GET', 'POST'])
def all_albums(request):
    parser_classes = (FileUploadParser,)
    if request.method == "GET":

        token = request.META.get('HTTP_AUTHORIZATION')
        if len(Token.objects.filter(key=token[7:])) == 0:
            return HttpResponseForbidden("Login Again")
        user = Token.objects.get(key=token[7:]).user_id
        albums = Album.objects.filter(privacy="public")
        albums_json = []
        for i in albums:
            likes = len(LikeAlbum.objects.filter(liked_to=i))
            liked = False
            if LikeAlbum.objects.filter(liked_to=i).filter(user_id=user):
                liked = True
            description = i.description
            name = i.name
            createdAt = i.created_at.strftime('%Y-%m-%d at %I:%M %p')
            cover_photo = i.cover_photo.name
            albums_json.append(
                {'id': i.id, 'name': name, 'description': description, 'likes': likes,
                 'liked': liked, 'createdAt': createdAt, 'coverPic': "http://127.0.0.1:8000/api/" + cover_photo})
        # ss = Ser(albums, many=True)
        # print(ss.data)
        return Response(albums_json, content_type="image/*")
    if request.method == "POST":
        like(request)


def create_album(request):
    print("create_album")


@login_required(login_url='/login/')
def like(request):
    if request.method == "POST":
        pid = request.POST["post_id"]
        username = request.POST["user"]
        is_photo = request.POST["is_photo"]

        user = User.objects.get(username=username)

        if is_photo:
            if LikePhoto.objects.filter(user=user).filter(liked_to=pid):
                LikePhoto.objects.filter(user=user).filter(liked_to=pid).delete()
            else:
                LikePhoto.objects.create(user=user, liked_to_id=pid)

        else:
            if LikeAlbum.objects.filter(user=user).filter(liked_to=pid):
                LikeAlbum.objects.filter(user=user).filter(liked_to=pid).delete()
            else:
                LikeAlbum.objects.create(user=user, liked_to_id=pid)

        return Response(
            data="done",
            status=status.HTTP_201_CREATED
        )


@login_required(login_url='/login/')
def upload(request):
    username = request.POST["user"]
    is_photo = request.POST["is_photo"]
    description = request.POST["description"]
    privacy = request.POST["privacy"]
    user = User.objects.get(username=username)
    photo = request.POST["picture"]
    if is_photo:
        album_id = request.POST["album_id"]
        Photo.objects.create(name=photo, description=description, privacy=privacy, user=user, album=album_id)
    else:
        album_name = request.POST["album_name"]
        Album.objects.create(name=album_name, description=description, privacy=privacy, user=user, cover_photo=photo)


CLIENT_ID = 'FSqpVDjXPQVhqeNYth6IQQI8eisLkcWTULTCeMN8'
CLIENT_SECRET = '3h1j9enpAGPkiOnnG6j2iCwkjCHXxbR6i6RDEPkXsbusGM97cvYxUs5x1tQmVelVXwUI6YqWGQyArIUHRHYyfKAURc8Cz38H69kEEynrqOCfUOhHHz9KxXfikQ5fiZKE'


@api_view(['POST'])
@csrf_exempt
def login(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    username = body["username"]
    password = body["password"]
    if len(Profile.objects.filter(user__username=username)) == 0:
        return HttpResponseBadRequest("invalid username")
    user = Profile.objects.get(user__username=username)
    if not check_password(password, user.user.password):
        return HttpResponseBadRequest("invalid username or password")
    if user:
        if Token.objects.get(user=user.user):
            Token.objects.get(user=user.user).delete()
    token = Token.objects.create(user=user.user)
    return Response({
        'token': token.key,
        'user_id': user.pk,
        'email': user.user.username
    })


@api_view(['POST'])
@csrf_exempt
def register(request):
    # print(request.POST['profilePic'])

    if request.FILES.get('profilePic') is not None:
        image_data = request.FILES['profilePic']
    else:
        image_data = None
    # format, imgstr = image_data.split(';base64,')
    # print("format", format)
    # ext = format.split('/')[-1]
    # data = ContentFile(base64.b64decode(imgstr))

    register_data = {'firstName': request.POST['firstName'], 'lastName': request.POST['lastName'],
                     'gender': request.POST['gender'], 'username': request.POST['username'],
                     'password': request.POST['password'], 'profilePic': image_data}
    print(register_data)

    # body_unicode = request.body.decode('utf-8')
    # body = json.loads(body_unicode)
    # print(body)
    profileSerializer = ProfileSerializer()
    return profileSerializer.create(register_data)


def logout_(request):
    logout(request)
    return HttpResponseRedirect('/home/')
