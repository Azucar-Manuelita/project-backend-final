from django.core.exceptions import ObjectDoesNotExist

from gym_core.repositories import workout_repository


def get_current_workout_plan(user_id: int) -> dict:

    active_plan = workout_repository.get_active_plan_by_user_id(user_id)

    if active_plan is None:
        raise ObjectDoesNotExist("The user does not have an active training plan.")

    plan_sessions = workout_repository.get_plan_sessions_with_completion(active_plan.id)

    sessions_detail = []
    completed_sessions = 0

    for plan_routine in plan_sessions:
        is_completed = plan_routine.workout_logs.exists()

        if is_completed:
            completed_sessions += 1

        sessions_detail.append(
            {
                "plan_routine_id": plan_routine.id,
                "session_number": plan_routine.session_number,
                "routine_name": plan_routine.routine.name,
                "is_completed": is_completed,
            }
        )

    total_sessions = len(sessions_detail)
    progress_percentage = (
        round((completed_sessions / total_sessions) * 100, 2)
        if total_sessions > 0
        else 0.0
    )

    return {
        "goal": active_plan.goal.name if active_plan.goal else None,
        "weekly_frequency": active_plan.weekly_frequency,
        "duration_weeks": active_plan.duration_weeks,
        "progress_percentage": progress_percentage,
        "sessions": sessions_detail,
    }


def toggle_session_completion(user_id: int, plan_routine_id: int) -> dict:
    """Marca una sesión (PlanRoutine) como completada creando un WorkoutLog,
    o la desmarca eliminando el WorkoutLog existente si ya estaba completada."""

    plan_routine = workout_repository.get_plan_routine_by_id(plan_routine_id)

    if plan_routine.plan.user_id != user_id:
        raise ObjectDoesNotExist("La sesión de entrenamiento no existe")

    existing_log = workout_repository.get_workout_log(plan_routine_id)

    if existing_log:
        workout_repository.delete_workout_log(existing_log)
        is_completed = False
    else:
        workout_repository.create_workout_log(plan_routine)
        is_completed = True

    return {
        "plan_routine_id": plan_routine.id,
        "is_completed": is_completed,
    }