from django import forms
from RateYourModule.models import Module, Review, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ReviewForm(forms.ModelForm):
    rating = forms.FloatField(min_value=0, max_value=5)
    message = forms.CharField(widget=forms.Textarea, max_length=200)

    class Meta:
        model = Review
        fields = ('rating', 'message',)

class SignUpForm(UserCreationForm):
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