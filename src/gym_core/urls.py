from django.urls import path
from gym_core.controllers import exercise_controllers

urlpatterns = [
    path('create_machine/', exercise_controllers.create_machine),
    path('create_exercise/', exercise_controllers.create_exercise)
]