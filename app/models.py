from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(default="photos/NA/user_default_thumb.jpg", upload_to="photos/")
    gender = models.CharField(max_length=15, default="Not Defined")

    def __str__(self):
        return self.user.username


class Album(models.Model):
    name = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=1000, null=True)
    cover_photo = models.ImageField(default="photos/NA/user_default_thumb.jpg", upload_to="photos/")
    privacy = models.CharField(max_length=10, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return str(self.id)


class Photo(models.Model):
    name = models.ImageField(upload_to="photos/")
    description = models.CharField(max_length=1000, null=True)
    privacy = models.CharField(max_length=10, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return str(self.id)


class LikeAlbum(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_to = models.ForeignKey(Album, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class LikePhoto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_to = models.ForeignKey(Photo, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

# python manage.py migrate --run-syncdb
