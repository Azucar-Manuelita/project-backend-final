from gym_core.models import GymUser, Goal, Limitation, UserLimitation

def register_user(correo, password_hash):
    user = GymUser(email=correo, password=password_hash)
    user.save()

def register_user_adittions(age, weight, user):
    user.age = age
    user.weight = weight
    user.save()

def get_user_by_correo(correo):
    try:
        return GymUser.objects.get(email=correo)
    except GymUser.DoesNotExist:
        return None
    

def check_password(user, password_hash):
    user = get_user_by_correo(user.email)
    if not user:
        return False
    if user.password == password_hash:
        return True
    return False

