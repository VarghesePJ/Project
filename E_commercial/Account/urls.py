from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.loginUser, name='login'),
    path('logout/',views.logoutUser, name='logout'),
    path('register/',views.Registration, name='register'),
    path('otp/',views.otp, name='otp'),
    path('profile/',views.profile, name='profile'),
]