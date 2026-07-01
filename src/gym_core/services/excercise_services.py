from gym_core.models import GymUser, TrainingPlan, UserAreaFitnessLevel

from gym_core.repositories import user_repository as user_repo
from gym_core.repositories import exercise_repository as exercise_repo
from gym_core.repositories import workout_repository as workout_repo


def validate_user_exists(user: GymUser | None):
    if user is None:
        raise ValueError("El usuario no existe")


def validate_user_levels(user: GymUser):
    if not user_repo.user_has_area_levels(user):
        raise ValueError("El usuario no tiene niveles por área asignados")


def validate_goal_exists(goal):
    if goal is None:
        raise ValueError("El objetivo no existe")


def validate_available_routines(routines: list, required: int = 1):
    if len(routines) < required:
        raise ValueError("No hay rutinas disponibles para este objetivo")


def apply_level_to_exercise(routine_exercise, user: GymUser) -> dict:
    exercise = routine_exercise.exercise
    area = exercise.muscular_area

    level_entry = (
        UserAreaFitnessLevel.objects
        .select_related("fitness_level")
        .filter(user=user, muscular_area=area)
        .first()
    )

    series = routine_exercise.series
    repetitions = routine_exercise.repetitions

    if level_entry:
        level = level_entry.fitness_level
        series = round(series * level.series_multiplier)
        repetitions = round(repetitions * level.repetitions_multiplier)

    return {
        "exercise": exercise,
        "series": series,
        "repetitions": repetitions,
    }

def build_personalized_exercises(routine_exercises: list, user: GymUser) -> list[dict]:
    return [apply_level_to_exercise(re, user) for re in routine_exercises]


def classify_user(user_id: int, area_id: int, level_id: int) -> UserAreaFitnessLevel:
    user = user_repo.get_user_by_id(user_id)
    validate_user_exists(user)

    area = exercise_repo.get_area_by_id(area_id)
    if area is None:
        raise ValueError("El área muscular no existe")

    level = exercise_repo.get_level_by_id(level_id)
    if level is None:
        raise ValueError("El nivel de condición física no existe")

    return user_repo.upsert_user_area_level(user, area, level)


def generate_training_plan(
    user_id: int,
    goal_id: int,
    weekly_frequency: int,
    duration_weeks: int,
    start_date,
) -> TrainingPlan:
    user = user_repo.get_user_by_id(user_id)
    validate_user_exists(user)
    validate_user_levels(user)

    goal = exercise_repo.get_goal_by_id(goal_id)
    validate_goal_exists(goal)

    routines = exercise_repo.get_goal_routines(goal)
    validate_available_routines(routines, required=1)

    plan = workout_repo.create_plan(
        user=user,
        goal=goal,
        weekly_frequency=weekly_frequency,
        duration_weeks=duration_weeks,
        start_date=start_date,
        status="active",
    )
    workout_repo.bulk_create_plan_routines(plan, routines)

    return plan


def adjust_training_plan(
    user_id: int,
    plan_id: int,
    weekly_frequency: int | None = None,
    duration_weeks: int | None = None,
) -> TrainingPlan:
    user = user_repo.get_user_by_id(user_id)
    validate_user_exists(user)

    plan = workout_repo.get_plan_by_id(plan_id)
    if plan is None:
        raise ValueError("El plan de entrenamiento no existe")
    if plan.user_id != user.id:
        raise ValueError("El plan no pertenece a este usuario")

    validate_user_levels(user)

    return workout_repo.update_plan(
        plan,
        weekly_frequency=weekly_frequency,
        duration_weeks=duration_weeks,
    )


def regenerate_plan_routines(user_id: int, plan_id: int) -> TrainingPlan:
    user = user_repo.get_user_by_id(user_id)
    validate_user_exists(user)

    plan = workout_repo.get_plan_by_id(plan_id)
    if plan is None:
        raise ValueError("El plan de entrenamiento no existe")
    if plan.user_id != user.id:
        raise ValueError("El plan no pertenece a este usuario")

    routines = exercise_repo.get_goal_routines(plan.goal)
    validate_available_routines(routines, required=1)

    workout_repo.delete_plan_routines(plan)
    workout_repo.bulk_create_plan_routines(plan, routines)

    return plan
