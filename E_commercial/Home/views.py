from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import AbstractUser

def Home(request):
    return render(request,"Home/home.html")