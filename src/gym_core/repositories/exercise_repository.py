from gym_core.models import MuscularArea, Machine, Exercise


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