from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls.static import static


from . import views

urlpatterns = [
    path('myalbums/', views.my_albums, name="user_albums"),
    path('albums/', views.all_albums, name="all_albums"),
    path('newalbum/', views.my_albums, name="new_albums"),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('register/', views.register, name='register'),
    path('photos/<str:name>', views.photo, name='photo')
]
