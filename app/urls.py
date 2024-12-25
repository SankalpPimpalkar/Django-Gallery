from django.urls import path
from .views import *

urlpatterns = [
    path('', get_images, name='home'),
    path('create-post', create_post, name='create_post'),
]
