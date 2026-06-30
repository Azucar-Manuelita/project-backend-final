import gym_core.repositories.user_repository as user_repository

def search_user(username):
    user = user_repository.get_user_by_username(username)
    if user:
        return {'success': True, 'user': user}
    return {'success': False, 'message': 'Usuario no encontrado'}

def update_user_info(age, weight, user):
    user_repository.register_user_adittions(age, weight, user)
    return {'success': True, 'message': 'Usuario actualizado exitosamente'}