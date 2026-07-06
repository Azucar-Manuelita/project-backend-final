from gym_core.models import (
    GymUser,
    Goal,
    Limitation,
    UserLimitation,
    TrainingPlan,
    UserAreaFitnessLevel,
    MuscularArea,
    FitnessLevel,
)

def register_user(correo, username, password_hash):
    user = GymUser(email=correo, username=username, password=password_hash, is_staff=False)
    user.save()

def register_user_adittions(user, weight, age):
    user.age = age
    user.weight = weight
    user.save()

def get_user_by_correo(email):
    return GymUser.objects.filter(email=email).first()

def get_user_by_username(username):
    return GymUser.objects.filter(username=username).first()

def get_user_by_id(user_id: int) -> GymUser | None:
    return GymUser.objects.filter(pk=user_id).first()

def get_goal_by_id(goal_id: int) -> Goal | None:
    return Goal.objects.filter(pk=goal_id).first()

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

def get_limitations():
    limitations = Limitation.objects.values_list('name', flat=True)
    return limitations

def get_muscular_areas():
    areas = MuscularArea.objects.values_list('name', flat=True)
    return areas

def get_limitations_by_user(user_id):
    limitations_user = UserLimitation.objects.filter(user_id=user_id).values_list('limitation__name', flat=True)
    return limitations_user

def get_areas_info_by_user(user_id):
    areas = UserAreaFitnessLevel.objects.filter(user_id=user_id).values_list('muscular_area__name','fitness_level__name')
    return areas

def update_user_limitations(user_id, limitations):
    UserLimitation.objects.filter(user_id=user_id).delete()
    for limitation in limitations:
        limitation_obj = Limitation.objects.filter(name=limitation).first()
        if limitation_obj:
            UserLimitation.objects.create(user_id=user_id, limitation=limitation_obj)

def update_user_areas(user_id, areas):
    UserAreaFitnessLevel.objects.filter(user_id=user_id).delete()
    for area in areas:
        area_obj = MuscularArea.objects.filter(name=area).first()
        if area_obj:
            UserAreaFitnessLevel.objects.create(user_id=user_id, muscular_area=area_obj)

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

def upsert_user_area_level(
    user: GymUser, area: MuscularArea, level: FitnessLevel
) -> UserAreaFitnessLevel:
    obj, _created = UserAreaFitnessLevel.objects.update_or_create(
        user=user,
        muscular_area=area,
        defaults={"fitness_level": level},
    )
    return obj

def user_has_area_levels(user: GymUser) -> bool:
    return UserAreaFitnessLevel.objects.filter(user=user).exists()

def get_all_users_with_plans() -> list:
    return list(
        GymUser.objects
        .prefetch_related("trainingplan_set")
        .order_by("id")
    )