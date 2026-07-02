import gym_core.repositories.user_repository as user_repository
from rest_framework.authtoken.models import Token

def search_user(username):
    user = user_repository.get_user_by_username(username)
    if user:
        return {'success': True, 'user': user}
    return {'success': False, 'message': 'Usuario no encontrado'}

def show_limitations():
    limitations = user_repository.get_limitations()
    if limitations:
        return {'success': True, 'message': limitations}
    return {'success': False, 'message': 'Limitaciones no encontradas'}

def show_areas():
    areas = user_repository.get_muscular_areas()
    if areas:
        return {'success': True, 'message': areas}
    return {'success': False, 'message': 'areas a evaluar no encontradas'}

def token_to_user(token):
    user_token = Token.objects.select_related('user').filter(key=token).first()
    if user_token:
        user=user_token.user
        return {'success': True, 'user': user}
    return {'success': False, 'message': "No existe un user con este token"}

def show_last_training_data(token):
    valid_token = token_to_user(token)
    if valid_token['success']:
        user = valid_token['user']
        limitations = user_repository.get_limitations_by_user(user.id)
        areas = user_repository.get_areas_info_by_user(user.id)
        data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "age": user.age,
            "weight": user.weight,
            "limitations": limitations,
            "areas": areas
        }
        return {'success': True, 'data': data}
    return {'success': False, 'error': valid_token['message']}

def update_user_info(user, weight, age, limitations, areas):
    user_repository.register_user_adittions(user, weight, age)
    user_repository.update_user_limitations(user.id, limitations)
    user_repository.update_user_areas(user.id, areas)
    return {'success': True, 'message': 'Usuario actualizado exitosamente'}
from gym_core.repositories import user_repository


def get_user_profile_service(user_id: int) -> dict:

    if user_id <= 0:
        return {"success": False, "message": "Invalid user ID"}

    raw_data = user_repository.get_user_profile_data(user_id)

    if raw_data is None:
        return {"success": False, "message": "User not found."}

    user = raw_data["user"]
    active_plan = raw_data["active_plan"]
    user_limitations = raw_data["user_limitations"]
    fitness_levels = raw_data["fitness_levels"]

    primary_goal = None
    days_per_week = None
    duration_weeks = None

    if active_plan:
        primary_goal = active_plan.goal.name if active_plan.goal else None
        days_per_week = active_plan.weekly_frequency
        duration_weeks = active_plan.duration_weeks

    physical_test_areas = [
        {
            "muscular_area": uafl.muscular_area.name,
            "fitness_level": uafl.fitness_level.name,
        }
        for uafl in fitness_levels
    ]

    limitations = [
        {
            "name": ul.limitation.name,
            "notes": ul.notes,
        }
        for ul in user_limitations
    ]

    # Mapeo de datos limpios
    profile_data = {
        "username": user.username,
        "email": user.email,
        "age": user.age,
        "weight": user.weight,
        "primary_goal": primary_goal,
        "secondary_goal": None,  # Pendiente de definición de modelo
        "physical_test_areas": physical_test_areas,
        "days_per_week": days_per_week,
        "duration_weeks": duration_weeks,
        "physical_limitations": limitations,
    }

    return {"success": True, "data": profile_data}
