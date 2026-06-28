from repositories import exercise_repository

def no_invalid_chars(name: str) -> bool:
    invalid_chars = set('!@#$%^&*()+=[]{}|\\;:"<>,.?/')
    return len(invalid_chars.intersection(name)) == 0
def valid_name_length(name: str) -> bool:
    return 1 <= len(name) <= 50
def correct_description_length(description: str) -> bool:
    return len(description) <= 500

def create_exercise(name: str, description: str, muscular_area, machine):
    if not no_invalid_chars(name):
        raise ValueError("Name contains invalid characters.")
    if not valid_name_length(name):
        raise ValueError("Name must be between 1 and 50 characters.")
    if not correct_description_length(description):
        raise ValueError("Description must be 500 characters or less.")

    return exercise_repository.save_exercise(name, description, muscular_area, machine)
