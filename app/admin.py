from django.contrib import admin
from .models import Owner, Album, Photo, Likes

admin.site.register(Owner)
admin.site.register(Album)
admin.site.register(Photo)
admin.site.register(Likes)
