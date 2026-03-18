from django.urls import path
from RateYourModule import views

app_name = 'rateyourmodule'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/<str:username>', views.show_profile, name='show_profile'),
    path('profile/<str:username>/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/delete/', views.delete_profile, name='delete_profile'),
    path('modules/', views.module_list, name='modules'),
    path('modules/add', views.add_module, name='add_module'),
    path('modules/<str:moduleID>', views.show_module, name='show_module'),
]