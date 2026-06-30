from django.urls import path
from gym_core.controllers import auth_controllers
from gym_core.controllers import user_controllers
from gym_core.controllers import workout_controllers

urlpatterns = [
    path('login/', auth_controllers.login),
    path('register/', auth_controllers.create_user),
    path("api/users/profile/", user_controllers.get_user_profile, name="user-profile"),
    path("api/workouts/current/", workout_controllers.get_current_workout_plan, name="workout-current"),
]