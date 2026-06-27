from django.urls import path
from gym_core.controllers import auth_controllers

urlpatterns = [
    path('login/', auth_controllers.login),
    path('register/', auth_controllers.create_user),
]