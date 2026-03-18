from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Avg
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from RateYourModule.models import Module
from RateYourModule.forms import SignUpForm

def index(request):
    modules = Module.objects.annotate(rating=Avg("review__rating")).order_by("-rating")
    context_dict = {"modules": modules}

    response = render(request, "index.html", context=context_dict)
    return response


def user_login(request):
    return HttpResponse("temp login view")


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rateyourmodule:index')) 


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect(reverse("rateyourmodule:index"))
        else:
            print(form.errors)

    else:
        form = SignUpForm()

    context_dict = {"form": form}
    response = render(request, "register.html", context=context_dict)
    return response 


def show_profile(request, username):
    return HttpResponse("temp profile")


def module_list(request):
    modules = Module.objects.all()
    context_dict = {"modules": modules}

    response = render(request, "modules.html", context=context_dict)
    return response


def show_module(request, moduleID):
    #Added rating feature with "module"
    module = Module.objects.annotate(rating=Avg("review__rating")).get(moduleID=moduleID)    
    context_dict = {"module": module, "reviews": module.review_set.all()}

    response = render(request, "module.html", context=context_dict, )
    return response
