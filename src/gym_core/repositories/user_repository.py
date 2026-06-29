from gym_core.models import GymUser, Goal, Limitation, UserLimitation, TrainingPlan, UserAreaFitnessLevel

def register_user(correo, username, password_hash):
    user = GymUser(email=correo, username=username, password=password_hash)
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
    
def get_user_by_username(username):
    try:
        return GymUser.objects.get(username=username)
    except GymUser.DoesNotExist:
        return None

def check_user(user):
    if get_user_by_correo(user):
        return get_user_by_correo(user)
    if get_user_by_username(user):
        return get_user_by_username(user)
    return None

def check_password(user, password_hash):
    user = check_user(user)
    if not user:
        return False
    if user.password == password_hash:
        return True
    return False


def get_user_profile_data(user_id: int):

    user = GymUser.objects.filter(pk=user_id).first()

    if user is None:
        return None

    active_plan = (
        TrainingPlan.objects
        .select_related("goal")
        .filter(user=user, status="active")
        .first()
    )

    user_limitations = list(
        UserLimitation.objects
        .select_related("limitation")
        .filter(user=user)
    )

    fitness_levels = list(
        UserAreaFitnessLevel.objects
        .select_related("muscular_area", "fitness_level")
        .filter(user=user)
    )

    return {
        "user": user,
        "active_plan": active_plan,
        "user_limitations": user_limitations,
        "fitness_levels": fitness_levels,
    }