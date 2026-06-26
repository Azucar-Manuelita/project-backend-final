from src.gym_core.models import MuscularArea, Machine, Exercise


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