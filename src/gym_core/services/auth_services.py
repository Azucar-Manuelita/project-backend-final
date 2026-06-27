import gym_core.repositories.user_repository as user_repository
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

def existence_user(email, username):
    if user_repository.check_user(username):
        return {'Failure': True, 'message': 'El nombre de usuario ya esta en uso'}
    if user_repository.get_user_by_correo(email):
        return {'Failure': True, 'message': 'El correo electronico ya esta en uso'}
    return {'Failure': False}

def register_user(email, username, password):
    if not valid_password(password)['success']:
        return {'success': False, 'message': valid_password(password)['message']}
    if existence_user(username, email)['Failure']:
        return {'success': False, 'message': existence_user(username, email)['message']}
    password_hash = hash_password(password)
    user_repository.register_user(email, username, password_hash)
    return {'success': True, 'message': 'Usuario registrado exitosamente'}

def authenticate_user(user, password):
    if user_repository.check_user(user) is None:
        return {'success': False, 'message': 'Usuario no encontrado'}
    password_hash = hash_password(password)
    return {'success': user_repository.check_password(user, password_hash), 'message': 'Autenticacion exitosa' if user_repository.check_password(user, password_hash) else 'Contraseña incorrecta'}
