from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Avg
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import AuthenticationForm
from RateYourModule.models import Module, UserProfile, Review
from RateYourModule.forms import SignUpForm, UserForm, ProfileForm, ReviewForm
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
    profile_user = get_object_or_404(User, username=username)
    logged_in_user = request.user

    if (profile_user.username == logged_in_user.username or logged_in_user.is_staff):
        profile_user.delete()
    else:
        return redirect(reverse("rateyourmodule:show_profile", kwargs={"username": profile_user.username}))

    return redirect(reverse("rateyourmodule:index"))


def module_list(request):
    modules = Module.objects.all()
    context_dict = {"modules": modules}

    response = render(request, "modules.html", context=context_dict)
    return response


def show_module(request, moduleID):
    if request.method=="POST":
        action = request.POST.get("action")
        if action=="new_review":
            return add_review(request, moduleID)
        elif action=="edit_review":
            return edit_review(request, moduleID)
        elif action=="delete_review":
            return delete_review(request, moduleID)

    module = Module.objects.annotate(rating=Avg("review__rating")).get(moduleID=moduleID)    
    context_dict = {"module": module, "reviews": module.review_set.all()}

    response = render(request, "module.html", context=context_dict)
    return response


@staff_member_required
def add_module(request):
    return HttpResponse("temp module add view")

@login_required
def add_review(request, moduleID):
    module = get_object_or_404(Module, moduleID=moduleID)
    user_profile = UserProfile.objects.get(user=request.user)

    form = ReviewForm(request.POST)
    if form.is_valid():
        if Review.objects.filter(student=user_profile, module=module).exists():
            return HttpResponse("You have already reviewed this module.")
        review = form.save(commit=False)
        review.student = user_profile
        review.module = module
        from datetime import date
        review.date = date.today()
        review.save()
        messages.success(request, "Successfully added your review!")
        return redirect(reverse('rateyourmodule:show_module', kwargs={'moduleID': moduleID}))
    else:
        print(form.errors)


    context_dict = {'form': form, 'module': module}
    return redirect(reverse('rateyourmodule:show_module', kwargs={'moduleID': moduleID}))

@login_required
def edit_review(request, moduleID):
    user_profile = UserProfile.objects.get(user=request.user)
    reviewID = request.POST.get("reviewID")
    print(reviewID)
    review = Review.objects.filter(id=reviewID, student=user_profile).first()
    if review:
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            from datetime import date
            review.date = date.today()
            review.save()
            messages.success(request, "Successfully edited your review!")
        else:
            messages.error(request, "Form data invalid.")
            print(form.errors)
    else:
        messages.error(request, "This review was not created by you.")
    return redirect(reverse('rateyourmodule:show_module', kwargs={'moduleID': moduleID}))


@login_required
def delete_review(request, moduleID):
    user_profile = UserProfile.objects.get(user=request.user)
    reviewID = request.POST.get("reviewID")
    print(reviewID)
    review = Review.objects.filter(id=reviewID, student=user_profile).first()
    if review:
        review.delete()
        messages.success(request, "Successfully deleted your review!")
    else:
        messages.error(request, "This review was not created by you.")
    return redirect(reverse('rateyourmodule:show_module', kwargs={'moduleID': moduleID}))


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


def get_module_list(max_results=0, starts_with=''):
    module_list = []
    if starts_with:
        module_list = Module.objects.filter(short_name__istartswith=starts_with)

    if 0 < max_results < len(module_list):
        module_list = module_list[:max_results]
    
    return module_list


class ModuleSuggestionView(View):
    def get(self, request):
        if 'suggestion' in request.GET:
            suggestion = request.GET['suggestion']
        else:
            suggestion = ''
        
        module_list = get_module_list(max_results=0, starts_with=suggestion)

        return render(request, 'module_suggestions.html',{'modules':module_list})
    

