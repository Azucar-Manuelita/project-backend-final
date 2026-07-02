from django.urls import path
from gym_core.controllers import exercise_controllers

urlpatterns = [
    path('create_machine/', exercise_controllers.create_machine),
    path('create_exercise/', exercise_controllers.create_exercise),
    path('exercises_by_machine/<str:machine_name>/', exercise_controllers.get_exercises_by_machine),
    path('machines/', exercise_controllers.get_machines),
    path('exercises/', exercise_controllers.get_exercises)
]