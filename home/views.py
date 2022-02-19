from ast import Pass
from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm


def index(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        d_password = request.POST.get("d_password")

        
        print(name)
    return render(request=request, template_name="home/index.html")