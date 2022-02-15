from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from maxminddb import Reader


def index(request):
    return render(request,'home/index.html')