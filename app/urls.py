from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token


from . import views

urlpatterns = [
    path('albums/', views.public_albums, name="all_albums"),
    path('album/', views.album, name="album"),
    path('deletealbum/<str:name>', views.delete_album, name="delete Album"),

    path('pic/<str:photo>', views.picture, name='photo'),
    path('photo/<str:album>', views.photo, name="photo"),
    path('deletepic/<str:name>', views.delete_pic, name="delete Album"),

    path('like/', views.like, name="like"),

    path('register/', views.register, name='register'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('deleteuser', views.delete_user, name="delete Album"),

    path('photos/<str:name>', views.cover_pho, name='photo'),
    path('pics/photos/<str:name>', views.album_pho, name='photo'),
]
