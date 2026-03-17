from django.contrib import admin
from RateYourModule.models import UserProfile, Module, Review

admin.site.register(Module)
admin.site.register(Review)
admin.site.register(UserProfile)