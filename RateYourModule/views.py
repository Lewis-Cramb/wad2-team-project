from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Avg
from django.urls import reverse
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import AuthenticationForm
from RateYourModule.models import Module, UserProfile, Review
from RateYourModule.forms import SignUpForm, UserForm, ProfileForm
from django.utils.decorators import method_decorator
from django.views import View

def index(request):
    modules = Module.objects.annotate(rating=Avg("review__rating")).order_by("-rating")
    context_dict = {"modules": modules}

    response = render(request, "index.html", context=context_dict)
    return response


def user_login(request):
    if (request.method == "POST"):
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(reverse("rateyourmodule:index"))
    else:
        form = AuthenticationForm()

    context_dict = {"form": form}
    return render(request, "login.html", context_dict)


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse("rateyourmodule:index")) 


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
    user_object = get_object_or_404(User, username=username)
    user_profile = UserProfile.objects.get_or_create(user=user_object)[0]
    reviews = Review.objects.filter(student=user_profile)
    user_form = UserForm(instance=user_object)
    profile_form = ProfileForm(instance=user_profile)

    context_dict = {"profile": user_profile, "reviews": reviews, "user_form":user_form, "profile_form":profile_form}
    response = render(request, "profile.html", context=context_dict)
    return response


@login_required
def edit_profile(request, username):
    return HttpResponse("Edit profile not implemented yet")


@login_required
def delete_profile(request, username):
    return HttpResponse("Delete profile not implemented yet")


def module_list(request):
    modules = Module.objects.all()
    context_dict = {"modules": modules}

    response = render(request, "modules.html", context=context_dict)
    return response


def show_module(request, moduleID):
    module = Module.objects.annotate(rating=Avg("review__rating")).get(moduleID=moduleID)    
    context_dict = {"module": module, "reviews": module.review_set.all()}

    response = render(request, "module.html", context=context_dict)
    return response


@staff_member_required
def add_module(request):
    return HttpResponse("temp module add view")

class LikeReviewView(View):
    @method_decorator(login_required)
    def get(self, request):
        review_id = request.GET.get('review_id')

        try:
            review = Review.objects.get(id=review_id)
        except Review.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)
        
        liked_reviews = request.session.get('liked_reviews', [])

        if review_id not in liked_reviews:
            review.likes += 1
            review.save()
            liked_reviews.append(review_id)
            request.session['liked_reviews'] = liked_reviews

        return HttpResponse(review.likes)

