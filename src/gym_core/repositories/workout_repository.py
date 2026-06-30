from gym_core.models import TrainingPlan, PlanRoutine


def get_active_plan_by_user_id(user_id):
    return (
        TrainingPlan.objects
        .select_related("goal")
        .filter(user_id=user_id, status="active")
        .first()
    )


def get_plan_sessions_with_completion(plan_id):

    return (
        PlanRoutine.objects
        .select_related("routine")
        .filter(plan_id=plan_id)
        .prefetch_related("workout_logs")
        .order_by("session_number")
    )