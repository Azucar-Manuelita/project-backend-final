from rest_framework import serializers


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