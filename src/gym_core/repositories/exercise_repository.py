from gym_core.models import (
    MuscularArea,
    Machine,
    Exercise,
    Goal,
    GoalRoutine,
    Routine,
    RoutineExercise,
    FitnessLevel,
    PlanRoutine,
    ExerciseLimitation,
    UserAreaFitnessLevel,
)

def save_exercise(name: str, description: str, muscular_area: str, machine: str):
    area_obj = MuscularArea.objects.filter(name=muscular_area).first()
    machine_obj = Machine.objects.filter(name=machine).first()
    return Exercise.objects.create(
        name=name,
        description=description,
        muscular_area=area_obj,
        machine=machine_obj
    )

def get_exercise_by_name(name: str):
    return Exercise.objects.filter(name=name).first()

def get_exercises_by_machine(machine: str):
    return Exercise.objects.filter(machine=Machine.objects.filter(name=machine).first())

def save_machine(name: str):
    return Machine.objects.create(name=name)

def get_machine_by_name(name: str):
    return Machine.objects.filter(name=name).first()

def get_machines():
    return Machine.objects.all()

def get_exercises():
    return Exercise.objects.all()

def get_area_by_id(area_id: int) -> MuscularArea | None:
    return MuscularArea.objects.filter(pk=area_id).first()

def get_level_by_id(level_id: int) -> FitnessLevel | None:
    return FitnessLevel.objects.filter(pk=level_id).first()

def get_goal_by_id(goal_id: int) -> Goal | None:
    return Goal.objects.filter(pk=goal_id).first()

def get_all_goals() -> list[Goal]:
    return list(Goal.objects.all())

def get_all_areas() -> list[MuscularArea]:
    return list(MuscularArea.objects.all())

def get_all_fitness_levels() -> list[FitnessLevel]:
    return list(FitnessLevel.objects.all())

def get_goal_routines(goal: Goal) -> list[Routine]:
    return list(
        Routine.objects.filter(goalroutine__goal=goal)
    )

def get_exercises_from_routines(routines: list[Routine]):
    return list(
        RoutineExercise.objects
        .select_related("exercise", "exercise__muscular_area", "routine")
        .filter(routine__in=routines)
    )


def get_plan_routine_by_id(plan_routine_id: int) -> PlanRoutine:

    return (
        PlanRoutine.objects
        .select_related("plan", "plan__user", "routine")
        .get(pk=plan_routine_id)
    )


def get_routine_exercise_detail(routine_id: int, exercise_id: int) -> RoutineExercise:

    return (
        RoutineExercise.objects
        .select_related(
            "exercise",
            "exercise__muscular_area",
            "exercise__machine",
        )
        .get(routine_id=routine_id, exercise_id=exercise_id)
    )


def exercise_is_excluded_for_user(exercise_id: int, user_id: int) -> bool:

    return (
        ExerciseLimitation.objects
        .filter(
            exercise_id=exercise_id,
            limitation__userlimitation__user_id=user_id,
        )
        .exists()
    )


def get_user_area_fitness_level(user_id: int, muscular_area_id: int) -> UserAreaFitnessLevel | None:

    return (
        UserAreaFitnessLevel.objects
        .select_related("fitness_level")
        .filter(user_id=user_id, muscular_area_id=muscular_area_id)
        .first()
    )

def get_routine_exercises_by_routine_id(routine_id: int):

    return (
        RoutineExercise.objects
        .select_related(
            "exercise",
            "exercise__muscular_area",
            "exercise__machine",
        )
        .filter(routine_id=routine_id)
    )
