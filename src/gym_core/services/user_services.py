from django.core.exceptions import ObjectDoesNotExist

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


def get_user_profile_by_admin_service(target_user_id: int) -> dict:

    if target_user_id <= 0:
        return {"success": False, "message": "Invalid user ID"}

    raw_data = user_repository.get_user_profile_data(target_user_id)

    if raw_data is None:
        raise ObjectDoesNotExist("El usuario solicitado no existe.")

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

def get_all_users_summary_service() -> dict:

    users = user_repository.get_all_users_with_plans()

    users_summary = []

    for user in users:
        has_active_plan = any(
            plan.status == "active" for plan in user.trainingplan_set.all()
        )
        plan_status = "Active" if has_active_plan else "Inactive"

        users_summary.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "plan_status": plan_status,
        })

    return {"success": True, "data": users_summary}