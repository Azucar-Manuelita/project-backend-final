from repositories import exercise_repository

def no_invalid_chars(name: str) -> bool:
    invalid_chars = set('!@#$%^&*()+=[]{}|\\;:"<>,.?/')
    return len(invalid_chars.intersection(name)) == 0

def valid_name_length(name: str) -> bool:
    return 1 <= len(name) <= 50

def correct_description_length(description: str) -> bool:
    return len(description) <= 500

def is_valid_muscular_area(area: str) -> bool:
    if area not in ["Brazos", "Pecho", "Espalda", "Abdomen", "Piernas", "Cardio"]:
        return False
    return True

def exists_machine(name: str) -> bool:
    if exercise_repository.get_machine_by_name(name) is None:
        return False
    return True

def is_valid_exercise(name: str, description: str, area: str, machine: str) -> bool:
    if not no_invalid_chars(name):
        return False
    if not valid_name_length(name):
        return False
    if not correct_description_length(description):
        return False
    if not is_valid_muscular_area(area):
        return False
    if not exists_machine(machine):
        return False
    return True

def create_exercise(name: str, description: str, area: str, machine: str):
    if is_valid_exercise(name, description, area, machine):
        return exercise_repository.save_exercise(name, description, area, machine)
    return False

def is_valid_machine(name: str) -> bool:
    if not no_invalid_chars(name):
        return False
    if not valid_name_length(name):
        return False
    return True

def create_machine(name: str):
    if is_valid_machine(name):
        return exercise_repository.save_machine(name)
    return False

