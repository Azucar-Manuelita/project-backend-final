from django.urls import path
from gym_core.controllers import auth_controllers
from gym_core.controllers import user_controllers
from gym_core.controllers import workout_controllers
from gym_core.controllers import excercise_controllers

urlpatterns = [
    path('login/', auth_controllers.login),
    path('register/', auth_controllers.create_user),
    path("api/users/profile/", user_controllers.get_user_profile, name="user-profile"),
    path("api/admin/users/<int:user_id>/profile/", user_controllers.get_user_profile_by_admin, name="admin-user-profile"),
    path("api/workouts/current/", workout_controllers.get_current_workout_plan, name="workout-current"),
    path("api/exercises/<int:exercise_id>/", excercise_controllers.exercise_detail, name="exercise-detail"),
    path("api/workouts/sessions/<int:plan_routine_id>/exercises/", excercise_controllers.session_exercises_list, name="session-exercises-list"),
]