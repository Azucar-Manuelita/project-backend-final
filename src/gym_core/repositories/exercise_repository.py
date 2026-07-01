from gym_core.models import (
    MuscularArea,
    Machine,
    Exercise,
    Goal,
    GoalRoutine,
    Routine,
    RoutineExercise,
    FitnessLevel,
)

def save_exercise(name: str, description: str, muscular_area: MuscularArea, machine: Machine):
    return Exercise.objects.create(
        name=name,
        description=description,
        muscular_area=muscular_area,
        machine=machine
    )

def get_exercise_by_name(name: str) -> Exercise:
    return Exercise.objects.get(name=name)

def save_machine(name: str) -> Machine:
    return Machine.objects.create(name=name)

def get_machine_by_name(name: str) -> Machine:
    return Machine.objects.get(name=name)

def get_area_by_id(area_id: int) -> MuscularArea | None:
    return MuscularArea.objects.filter(pk=area_id).first()

def get_level_by_id(level_id: int) -> FitnessLevel | None:
    return FitnessLevel.objects.filter(pk=level_id).first()

def get_goal_by_id(goal_id: int) -> Goal | None:
    return Goal.objects.filter(pk=goal_id).first()

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
