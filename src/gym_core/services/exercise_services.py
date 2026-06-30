from gym_core.repositories import exercise_repository

def exists_machine(name: str) -> bool:
    return exercise_repository.get_machine_by_name(name) is not None

def is_exercise_in_machine(exercise_name: str, machine_name: str) -> bool:
    exercises = exercise_repository.get_exercises_by_machine(machine_name)
    for exercise in exercises:
        if exercise.name == exercise_name:
            return True
    return False

def create_exercise(name: str, description: str, area: str, machine: str):
    if not exists_machine(machine):
        return False
    if is_exercise_in_machine(name, machine):
        return False
    return exercise_repository.save_exercise(name, description, area, machine)

def create_machine(name: str):
    if exists_machine(name):
        return False
    return exercise_repository.save_machine(name)
