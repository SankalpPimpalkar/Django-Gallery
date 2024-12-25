from django.urls import path
from .views import *

urlpatterns = [
    path('register/', create_user, name='create_user'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user'),
    path('profile/', profile, name='profile_user'),
    path('edit-profile/', edit_profile, name='edit_profile'),
]
