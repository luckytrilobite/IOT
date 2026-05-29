from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, "web/home.html")

def about(request):
    return render(request, "web/about.html")

def dashboard(request):
    return render(request, "web/dashboard.html")