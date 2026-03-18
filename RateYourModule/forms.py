from django import forms
from RateYourModule.models import Review

class ReviewForm(forms.ModelForm):
    rating = forms.FloatField(min_value=0, max_value=5)
    message = forms.CharField(widget=forms.Textarea, max_length=200)

    class Meta:
        model = Review
        fields = ('rating', 'message',)