from django.contrib import admin
from .models import Profile, Album, Photo, LikeAlbum, LikePhoto

admin.site.register(Profile)
admin.site.register(Album)
admin.site.register(Photo)
admin.site.register(LikePhoto)
admin.site.register(LikeAlbum)
