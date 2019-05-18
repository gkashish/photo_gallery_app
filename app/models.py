from django.db import models


class Owner(models.Model):
    username = models.CharField(max_length=255, null=False)
    name = models.CharField(max_length=255, null=False)


class Album(models.Model):
    name = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=1000, null=True)
    cover_photo = models.CharField(max_length=1000, null=True)
    privacy = models.CharField(max_length=255, null=False)
    username = models.CharField(max_length=255, null=False)
    created_on = models.DateField(max_length=255, null=False)


class Photo(models.Model):
    name = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=1000, null=True)
    privacy = models.CharField(max_length=255, null=False)
    username = models.CharField(max_length=255, null=False)
    album = models.CharField(max_length=255, null=False)
    created_on = models.DateField(max_length=255, null=False)


class Likes(models.Model):
    liked_by = models.CharField(max_length=255, null=False)
    username = models.CharField(max_length=255, null=False)
    album = models.CharField(max_length=255, null=False)
    song = models.CharField(max_length=255, null=False)
