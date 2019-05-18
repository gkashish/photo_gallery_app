from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from rest_framework.response import Response
from rest_framework import status

from .models import Profile, Album, Photo, LikeAlbum, LikePhoto
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from .serializers import LikePhotoSerializer


def re(request):
    return redirect("/home/")


@login_required(login_url='/login/')
def home(request):
    print(request.user.username)

    if request.user.username:
        if User.objects.filter(username=request.user.username).exists():
            user = User.objects.get(username=request.user.username)
        else:
            return HttpResponse("No user exist with this username.")
    else:
        user = request.user

    albums = Album.objects.filter(user=user)
    likes, liked = [], []
    for i in albums:
        print(i.name)
        likes.append(len(LikeAlbum.objects.filter(liked_to=i)))
        if LikeAlbum.objects.filter(liked_to=i).filter(user=request.user):
            liked.append(True)
        else:
            liked.append(False)
    # top_posts = posts[:10]
    # top_posts = Post.objects.filter(user=user).order_by('-id')
    string = "Welcome " + request.user.username
    print(string)
    # return render(request, "home.html", {"user": user, "post": top_posts, "Message": string, "like_list": like_list,
    #                                      "dislike_list": dislike_list, "comments_list": comments_list})


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
