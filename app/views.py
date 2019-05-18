import json

from django.core import serializers
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from rest_framework.response import Response
from rest_framework import status

from .models import Profile, Album, Photo, LikeAlbum, LikePhoto
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from .serializers import AlbumSerializer


# def re(request):
#     return redirect("/home/")


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
