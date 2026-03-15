from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Avg
from RateYourModule.models import Module

def index(request):
    modules = Module.objects.annotate(rating=Avg("review__rating")).order_by("-rating")
    context_dict = {"modules": modules}

    response = render(request, "index.html", context=context_dict)
    return response


def user_login(request):
    return HttpResponse("temp login view")


def user_logout(request):
    return HttpResponse("temp logout view")


def signup(request):
    return HttpResponse("temp signup view")


def show_profile(request, username):
    return HttpResponse("temp profile")


def module_list(request):
    modules = Module.objects.all()
    context_dict = {"modules": modules}

    response = render(request, "modules.html", context=context_dict)
    return response


def show_module(request, moduleID):
    module = Module.objects.get(moduleID=moduleID)
    context_dict = {"module": module, "reviews": module.review_set.all()}

    response = render(request, "module.html", context=context_dict)
    return response
