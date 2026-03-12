from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("temp index view")

def user_login(request):
    return HttpResponse("temp login view")

def user_logout(request):
    return HttpResponse("temp logout view")

def signup(request):
    return HttpResponse("temp signup view")

