from django import forms
from RateYourModule.models import Module, Review, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ReviewForm(forms.ModelForm):
    rating = forms.FloatField(min_value=0, max_value=5)
    message = forms.CharField(widget=forms.Textarea, max_length=200, required=False)

    class Meta:
        model = Review
        fields = ('rating', 'message',)

class ModuleForm(forms.ModelForm):
    moduleID = forms.CharField(max_length=20)
    short_name = forms.CharField(max_length=20)
    full_name = forms.CharField(max_length=50)

    class Meta:
        model = Module
        fields = ('moduleID','short_name','full_name')

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = ''

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class SignUpForm(CustomUserCreationForm):
    email = forms.EmailField(required=True)
    picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
            UserProfile.objects.create(user=user, picture=self.cleaned_data.get("picture"))

        return user


# Edit User details
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]


# Edit UserProfile details
class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["picture"]