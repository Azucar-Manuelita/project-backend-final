from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from gym_core.services import excercise_services
from gym_core.serializers import excercise_serializers


def _error_status_code(message: str) -> int:
    return 404 if "no existe" in message.lower() else 400


@api_view(["POST"])
def classify_user(request):
    serializer = excercise_serializers.ClassifyUserSerializer(data=request.data)

    if not serializer.is_valid():
        return Response({"code": 400, "error": "Campos requeridos"})

    user_id = request.user.id
    result = excercise_services.classify_user(
        user_id,
        serializer.validated_data["area_id"],
        serializer.validated_data["level_id"],
    )

    if not result["success"]:
        error_message = result["message"]
        return Response({"code": _error_status_code(error_message), "error": error_message})

    output = excercise_serializers.UserAreaFitnessLevelSerializer(result["data"])
    return Response({"code": 201, "data": output.serialize()})


@api_view(["POST"])
def generate_training_plan(request):
    serializer = excercise_serializers.GenerateTrainingPlanSerializer(data=request.data)

    if not serializer.is_valid():
        return Response({"code": 400, "error": "Campos requeridos"})

    user_id = request.user.id
    result = excercise_services.generate_training_plan(
        user_id=user_id,
        goal_id=serializer.validated_data["goal_id"],
        weekly_frequency=serializer.validated_data["weekly_frequency"],
        duration_weeks=serializer.validated_data["duration_weeks"],
        start_date=serializer.validated_data["start_date"],
    )

    if not result["success"]:
        error_message = result["message"]
        return Response({"code": _error_status_code(error_message), "error": error_message})

    output = excercise_serializers.TrainingPlanSerializer(result["data"])
    return Response({"code": 201, "data": output.serialize()})


@api_view(["PATCH"])
def adjust_training_plan(request):
    serializer = excercise_serializers.AdjustTrainingPlanSerializer(data=request.data)

    if not serializer.is_valid():
        return Response({"code": 400, "error": "Campos requeridos"})

    user_id = request.user.id
    result = excercise_services.adjust_training_plan(
        user_id=user_id,
        plan_id=serializer.validated_data["plan_id"],
        weekly_frequency=serializer.validated_data.get("weekly_frequency"),
        duration_weeks=serializer.validated_data.get("duration_weeks"),
    )

    if not result["success"]:
        error_message = result["message"]
        return Response({"code": _error_status_code(error_message), "error": error_message})

    output = excercise_serializers.TrainingPlanSerializer(result["data"])
    return Response({"code": 200, "data": output.serialize()})


@api_view(["POST"])
def regenerate_plan_routines(request):
    serializer = excercise_serializers.RegeneratePlanRoutinesSerializer(data=request.data)

    if not serializer.is_valid():
        return Response({"code": 400, "error": "Campos requeridos"})

    user_id = request.user.id
    result = excercise_services.regenerate_plan_routines(
        user_id=user_id,
        plan_id=serializer.validated_data["plan_id"],
    )

    if not result["success"]:
        error_message = result["message"]
        return Response({"code": _error_status_code(error_message), "error": error_message})

    output = excercise_serializers.TrainingPlanSerializer(result["data"])
    return Response({"code": 200, "data": output.serialize()})


@api_view(["GET"])
def exercise_detail(request, exercise_id):
    plan_routine_id = int(request.query_params.get("plan_routine_id"))

    detail_data = excercise_services.get_exercise_detail_service(
        user=request.user,
        exercise_id=exercise_id,
        plan_routine_id=plan_routine_id,
    )

    output = excercise_serializers.ExerciseDetailSerializer(detail_data)
    return Response({"code": 200, "data": output.serialize()}, status=status.HTTP_200_OK)

@api_view(["GET"])
def session_exercises_list(request, plan_routine_id):
    session_exercises = excercise_services.get_session_exercises_list_service(
        user=request.user,
        plan_routine_id=plan_routine_id,
    )

    output = excercise_serializers.SessionExerciseListSerializer(session_exercises)
    return Response({"code": 200, "data": output.serialize()}, status=status.HTTP_200_OK)