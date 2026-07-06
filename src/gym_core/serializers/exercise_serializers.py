from rest_framework import serializers
from gym_core.services.exercise_services import exists_machine

def no_invalid_chars(name: str) -> bool:
    invalid_chars = set('!@#$%^&*()+=[]{}|\\;:"<>,.?/')
    return len(invalid_chars.intersection(name)) == 0

class exercise_serializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=500)
    area = serializers.ChoiceField(choices=["Brazos", "Pecho", "Espalda", "Abdomen", "Piernas", "Cardio"])
    machine = serializers.CharField(max_length=50)

    def validate_name(self, value):
        if not no_invalid_chars(value):
            raise serializers.ValidationError("El nombre contiene caracteres inválidos.")
        return value
    def validate_machine(self, value):
        if not exists_machine(value):
            raise serializers.ValidationError("Maquina no encontrada.")
        return value

class machine_serializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)

    def validate_name(self, value):
        if not no_invalid_chars(value):
            raise serializers.ValidationError("El nombre contiene caracteres inválidos.")
        return value
    

class exercise_response_serializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
    area = serializers.CharField(source='muscular_area.name') 
    machine = serializers.CharField(source='machine.name')

class ClassifyUserSerializer(serializers.Serializer):
    area_id = serializers.IntegerField()
    level_id = serializers.IntegerField()


class GenerateTrainingPlanSerializer(serializers.Serializer):
    goal_id = serializers.IntegerField()
    weekly_frequency = serializers.IntegerField(min_value=1)
    duration_weeks = serializers.IntegerField(min_value=1)
    start_date = serializers.DateField()


class AdjustTrainingPlanSerializer(serializers.Serializer):
    plan_id = serializers.IntegerField()
    weekly_frequency = serializers.IntegerField(min_value=1, required=False)
    duration_weeks = serializers.IntegerField(min_value=1, required=False)


class RegeneratePlanRoutinesSerializer(serializers.Serializer):
    plan_id = serializers.IntegerField()


class UserAreaFitnessLevelSerializer:

    def __init__(self, level_obj):
        self._obj = level_obj

    def serialize(self) -> dict:
        return {
            "muscular_area": self._obj.muscular_area.name,
            "fitness_level": self._obj.fitness_level.name,
        }


class TrainingPlanSerializer:

    def __init__(self, plan_obj):
        self._obj = plan_obj

    def serialize(self) -> dict:
        return {
            "id": self._obj.id,
            "goal": self._obj.goal.name,
            "weekly_frequency": self._obj.weekly_frequency,
            "duration_weeks": self._obj.duration_weeks,
            "start_date": self._obj.start_date.isoformat(),
            "status": self._obj.status,
        }


class ExerciseDetailSerializer:

    def __init__(self, detail_data: dict):
        self._data = detail_data

    def serialize(self) -> dict:
        exercise = self._data["exercise"]
        return {
            "id": exercise.id,
            "name": exercise.name,
            "description": exercise.description,
            "machine_name": self._data["machine_name"],
            "series": self._data["series"],
            "repetitions": self._data["repetitions"],
        }
    

class SessionExerciseListSerializer:

    def __init__(self, session_exercises: list[dict]):
        self._data = session_exercises

    def serialize(self) -> list[dict]:
        return [
            {
                "id": item["exercise"].id,
                "name": item["exercise"].name,
                "machine_name": item["machine_name"],
                "series": item["series"],
                "repetitions": item["repetitions"],
            }
            for item in self._data
        ]