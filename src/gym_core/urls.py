from django.urls import path
from gym_core.controllers import auth_controllers
from gym_core.controllers import user_controllers
from gym_core.controllers import workout_controllers

urlpatterns = [
    path('login/', auth_controllers.login, name="login"),
    path('register/', auth_controllers.create_user, name="register"),
    path('api/users/profile/data/initial_call', user_controllers.show_initial_training_data, name="initial-call"),
    path('api/users/profile/data/latest_data', user_controllers.latest_user_training_data, name="latest-training-data"),
    path('api/users/profile/data/update_latest_data', user_controllers.update_user_training_data, name="update-latest-training-data"),
    path("api/users/profile/", user_controllers.get_user_profile, name="user-profile"),
    path("api/workouts/current/", workout_controllers.get_current_workout_plan, name="workout-current"),
]