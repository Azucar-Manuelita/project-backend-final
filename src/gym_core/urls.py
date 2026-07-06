from django.urls import path
from gym_core.controllers import auth_controllers
from gym_core.controllers import user_controllers
from gym_core.controllers import workout_controllers
from gym_core.controllers import exercise_controllers

urlpatterns = [
    path('login/', auth_controllers.login, name="login"),
    path('register/', auth_controllers.create_user, name="register"),
    path('api/users/profile/data/initial_call', user_controllers.show_initial_training_data, name="initial-call"),
    path('api/users/profile/data/latest_data', user_controllers.latest_user_training_data, name="latest-training-data"),
    path('api/users/profile/data/update_latest_data', user_controllers.update_user_training_data, name="update-latest-training-data"),
    path("api/users/profile/", user_controllers.get_user_profile, name="user-profile"),
    path("api/admin/users/<int:user_id>/profile/", user_controllers.get_user_profile_by_admin, name="admin-user-profile"),
    path("api/admin/users/", user_controllers.get_users_list_by_admin, name="admin-users-list"),
    path("api/workouts/current/", workout_controllers.get_current_workout_plan, name="workout-current"),
    path("api/exercises/<int:exercise_id>/", exercise_controllers.exercise_detail, name="exercise-detail"),
    path("api/workouts/sessions/<int:plan_routine_id>/exercises/", exercise_controllers.session_exercises_list, name="session-exercises-list"),
    path('create_machine/', exercise_controllers.create_machine),
    path('create_exercise/', exercise_controllers.create_exercise),
    path('exercises_by_machine/<str:machine_name>/', exercise_controllers.get_exercises_by_machine),
    path('machines/', exercise_controllers.get_machines),
    path('exercises/', exercise_controllers.get_exercises)
]