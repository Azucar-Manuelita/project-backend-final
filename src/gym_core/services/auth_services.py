import gym_core.repositories.user_repository as user_repository
from rest_framework.authtoken.models import Token
import hashlib

def valid_lenght(password):
    if len(password) < 8:
        return False
    return True

def valid_uppercase(password):
    for char in password:
        if char.isupper():
            return True
    return False

def valid_special_char(password):
    special_chars = "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~"
    for char in password:
        if char in special_chars:
            return True
    return False

def valid_number(password):
    for char in password:
        if char.isdigit():
            return True
    return False

def valid_password(password):
    if not valid_lenght(password):
        return {'success': False, 'message': 'La password debe tener al menos 8 caracteres'}
    if not valid_uppercase(password):
        return {'success': False, 'message': 'La password debe contener al menos una letra mayuscula'}
    if not valid_special_char(password):
        return {'success': False, 'message': 'La password debe contener al menos un caracter especial'}
    if not valid_number(password):
        return {'success': False, 'message': 'La password debe contener al menos un número'}
    return {'success': True, 'message': 'password valida'}

def hash_password(password):
    return hashlib.sha512(password.encode()).hexdigest()

def existence_user(email):
    if user_repository.check_user(email):
        return {'Failure': True, 'message': 'El correo electronico o nombre de usuario ya esta en uso'}
    return {'Failure': False}

def register_user(email, username, password):
    if not valid_password(password)['success']:
        return {'success': False, 'message': valid_password(password)['message']}
    if existence_user(email)['Failure']:
        return {'success': False, 'message': existence_user(email)['message']}
    password_hash = hash_password(password)
    user_repository.register_user(email, username, password_hash)
    token, created = Token.objects.get_or_create(user=user_repository.get_user_by_correo(email))
    return {'success': True, 'message': 'Usuario registrado exitosamente', 'token': token.key}

def authenticate_user(user, password):
    if user_repository.check_user(user) is None:
        return {'success': False, 'message': 'Usuario no encontrado'}
    password_hash = hash_password(password)
    user = user_repository.check_user(user)
    if user_repository.check_password(user, password_hash):
        token, created = Token.objects.get_or_create(user=user)
        return {'success': True, 'message': 'Autenticacion exitosa', 'token': token.key, 'staff': user.is_staff}
    return {'success': False, 'message': 'Contraseña incorrecta'}

