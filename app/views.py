import json

from django.core import serializers
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser

from .models import Profile, Album, Photo, LikeAlbum, LikePhoto
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from .serializers import AlbumSerializer,PhotoSerializer
from django.db.models import Q


# def re(request):
#     return redirect("/home/")



class AlbumsAPIView(APIView):
    parser_class = (FileUploadParser,)
    def get(self,request):
        #albums=Album.objects.filter(user=request.user)
        albums=Album.objects.filter(Q(user=request.user)|Q(privacy='public'))
        serializer = AlbumSerializer(albums,many=True)
        return Response({"albums":serializer.data})
    def post(self,request):
        data=request.data.copy()
        print(data)
        data['user']=request.user.pk
        album_serializer = AlbumSerializer(data=data)
        if album_serializer.is_valid():
            album_serializer.save()
            return Response(album_serializer.data,status=status.HTTP_201_CREATED)
        return Response(album_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class LikeAPIView(APIView):
    def post(self,request):
        if(request.data.get('type',None)==None or request.data.get('id',None)==None):
            return Response({"error":"Data is missing"},status=status.HTTP_400_BAD_REQUEST)
        obj_id=request.data.get('id',None)
        if(request.data.get('type',None)=='album'):
            try:
                album=Album.objects.get(pk=obj_id)
            except Album.DoesNotExist:
                return Response({"error":"Album id is wrong"},status=status.HTTP_400_BAD_REQUEST)
            is_liked = LikeAlbum.objects.filter(user=request.user.pk,liked_to=obj_id).count()
            if(is_liked):
                obj = LikeAlbum.objects.get(user=request.user,liked_to=album)
                obj.delete()
                c = LikeAlbum.objects.filter(liked_to=obj_id).count()
                return Response({"likes":c,"liked":False})
            else :
                obj = LikeAlbum.objects.create(user=request.user,liked_to=album)
                obj.save()
                c = LikeAlbum.objects.filter(liked_to=obj_id).count()
                return Response({"likes":c,"liked":True})
        if(request.data.get('type',None)=='photo'):
            try:
                photo = Photo.objects.get(pk=obj_id)
            except Photo.DoesNotExist:
                return Response({"error":"Photo id is wrong"},status=status.HTTP_400_BAD_REQUEST)
            is_liked = LikePhoto.objects.filter(user=request.user.pk,liked_to=obj_id).count()
            if(is_liked):
                obj = LikePhoto.objects.get(user=request.user,liked_to=obj_id)
                obj.delete()
                c = LikePhoto.objects.filter(liked_to=obj_id).count()
                return Response({"likes":c,"liked":False})
            else :
                obj = LikePhoto.objects.create(user=request.user,liked_to=obj_id)
                obj.save()
                c = LikePhoto.objects.filter(liked_to=obj_id).count()
                return Response({"likes":c,"liked":True})
        return Response({"error":"type is wrong!!"},status=status.HTTP_400_BAD_REQUEST)

class PhotosAPIView(APIView):
    def get(self,request,pk,format=None):
        photos = Photo.objects.filter(Q(album=pk)&(Q(user=request.user)|Q(privacy='public')))
        serializer = PhotoSerializer(photos,many=True)
        return Response({"photos":serializer.data},status=status.HTTP_201_CREATED)

class AddPhotoAPIView(APIView):
    parser_class = (FileUploadParser,)
    def get_object(self, pk):
        try:
            return Album.objects.get(pk=pk)
        except Album.DoesNotExist:
            raise Http404
    
    def post(self,request,pk,format=None):
        data=request.data
        data['user']=request.user.pk
        data['album']=pk
        serializer = PhotoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



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

    def get(self, request, pk,album, format=None):
        photo = self.get_object(pk)
        serializer = PhotoSerializer(photo)
        return Response(serializer.data)

    def delete(self, request, pk,album, format=None):
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
        data=request.data
        data['user']="1"
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


def all_albums(request):
    if request.method == "GET":
        albums = Album.objects.filter(privacy="public")
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


def login(request):
    print("login")


def new_user(request):
    print("New User")


def logout_(request):
    logout(request)
    return HttpResponseRedirect('/home/')
