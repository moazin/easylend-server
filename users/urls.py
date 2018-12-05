from django.urls import path

from . import views

urlpatterns = [
    path('newuser', views.UserCreateView.as_view()),
    path('myprofile', views.UserProfileView)
]