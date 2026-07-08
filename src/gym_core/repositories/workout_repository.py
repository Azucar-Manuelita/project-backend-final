from gym_core.models import TrainingPlan, PlanRoutine, GymUser, Goal, Routine, WorkoutLog


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

def get_plan_routine_by_id(plan_routine_id: int) -> PlanRoutine:
    return (
        PlanRoutine.objects
        .select_related("plan", "plan__user", "routine")
        .get(pk=plan_routine_id)
    )

def get_workout_log(plan_routine_id: int) -> WorkoutLog | None:
    return WorkoutLog.objects.filter(plan_routine_id=plan_routine_id).first()

def create_workout_log(plan_routine: PlanRoutine) -> WorkoutLog:
    return WorkoutLog.objects.create(plan_routine=plan_routine)

def delete_workout_log(workout_log: WorkoutLog):
    workout_log.delete()

def get_plan_by_id(plan_id: int) -> TrainingPlan | None:
    return TrainingPlan.objects.filter(pk=plan_id).first()

def create_plan(
    user: GymUser,
    goal: Goal,
    weekly_frequency: int,
    duration_weeks: int,
    start_date,
    status: str = "active",
) -> TrainingPlan:
    return TrainingPlan.objects.create(
        user=user,
        goal=goal,
        weekly_frequency=weekly_frequency,
        duration_weeks=duration_weeks,
        start_date=start_date,
        status=status,
    )

def bulk_create_plan_routines(plan: TrainingPlan, routines: list[Routine]) -> list[PlanRoutine]:
    plan_routines = [
        PlanRoutine(plan=plan, routine=routine, session_number=idx + 1)
        for idx, routine in enumerate(routines)
    ]
    return PlanRoutine.objects.bulk_create(plan_routines)

def delete_plan_routines(plan: TrainingPlan):
    PlanRoutine.objects.filter(plan=plan).delete()

def update_plan(
    plan: TrainingPlan,
    weekly_frequency: int | None = None,
    duration_weeks: int | None = None,
) -> TrainingPlan:
    if weekly_frequency is not None:
        plan.weekly_frequency = weekly_frequency
    if duration_weeks is not None:
        plan.duration_weeks = duration_weeks
    plan.save()
    return plan
