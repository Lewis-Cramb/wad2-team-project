from django.urls import path
from RateYourModule import views

app_name = 'rateyourmodule'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/<str:username>', views.show_profile, name='show_profile'),
    path('modules/', views.module_list, name='modules'),
    path('modules/<str:moduleID>', views.show_module, name='show_module'),
]