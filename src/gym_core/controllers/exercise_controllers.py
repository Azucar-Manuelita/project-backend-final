from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from gym_core.services import exercise_services
from gym_core.serializers import exercise_serializers
from rest_framework import status


@api_view(['POST'])
def create_exercise(request):
    serializer = exercise_serializers.ExerciseSerializer(data=request.data)
    if serializer.is_valid():
        name = serializer.validated_data['name']
        description = serializer.validated_data['description']
        area = serializer.validated_data['area']
        machine = serializer.validated_data['machine']

        if exercise_services.create_exercise(name, description, area, machine):
            return Response({"message": "Exercise created successfully."}, status=201)
        else:
            return Response({"error": "Failed to create exercise. It may already exist or the machine may not exist."}, status=400)
    else:
        return Response(serializer.errors, status=400)


@api_view(['POST'])
def create_machine(request):
    serializer = exercise_serializers.MachineSerializer(data=request.data)
    if serializer.is_valid():
        name = serializer.validated_data['name']

        if exercise_services.create_machine(name):
            return Response({"message": "Machine created successfully."}, status=201)
        else:
            return Response({"error": "Failed to create machine. It may already exist."}, status=400)
    else:
        return Response(serializer.errors, status=400)


@api_view(['GET'])
def get_exercises_by_machine(request, machine_name):
    exercises = exercise_services.get_exercises_by_machine(machine_name)
    serializer = exercise_serializers.ExerciseResponseSerializer(exercises, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_machines(request):
    machines = exercise_services.get_machines()
    serializer = exercise_serializers.MachineSerializer(machines, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_exercises(request):
    exercises = exercise_services.get_exercises()
    serializer = exercise_serializers.ExerciseResponseSerializer(exercises, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_goals_catalog(request):
    goals = exercise_services.get_goals_catalog()
    serializer = exercise_serializers.GoalCatalogSerializer(goals, many=True)
    return Response({"code": 200, "data": serializer.data})


@api_view(['GET'])
def get_areas_catalog(request):
    areas = exercise_services.get_areas_catalog()
    serializer = exercise_serializers.AreaCatalogSerializer(areas, many=True)
    return Response({"code": 200, "data": serializer.data})


@api_view(['GET'])
def get_fitness_levels_catalog(request):
    levels = exercise_services.get_fitness_levels_catalog()
    serializer = exercise_serializers.FitnessLevelCatalogSerializer(levels, many=True)
    return Response({"code": 200, "data": serializer.data})


def _error_status_code(message: str) -> int:
    return 404 if "no existe" in message.lower() else 400


@api_view(["POST"])
def classify_user(request):
    serializer = exercise_serializers.ClassifyUserSerializer(data=request.data)

    if not serializer.is_valid():
        return Response({"code": 400, "error": "Campos requeridos"})

    user_id = request.user.id
    result = exercise_services.classify_user(
        user_id,
        serializer.validated_data["area_id"],
        serializer.validated_data["level_id"],
    )

    if not result["success"]:
        error_message = result["message"]
        return Response({"code": _error_status_code(error_message), "error": error_message})

    output = exercise_serializers.UserAreaFitnessLevelSerializer(result["data"])
    return Response({"code": 201, "data": output.serialize()})


@api_view(["POST"])
def generate_training_plan(request):
    serializer = exercise_serializers.GenerateTrainingPlanSerializer(data=request.data)

    if not serializer.is_valid():
        return Response({"code": 400, "error": "Campos requeridos"})

    user_id = request.user.id
    result = exercise_services.generate_training_plan(
        user_id=user_id,
        goal_id=serializer.validated_data["goal_id"],
        weekly_frequency=serializer.validated_data["weekly_frequency"],
        duration_weeks=serializer.validated_data["duration_weeks"],
        start_date=serializer.validated_data["start_date"],
    )

    if not result["success"]:
        error_message = result["message"]
        return Response({"code": _error_status_code(error_message), "error": error_message})

    output = exercise_serializers.TrainingPlanSerializer(result["data"])
    return Response({"code": 201, "data": output.serialize()})


@api_view(["PATCH"])
def adjust_training_plan(request):
    serializer = exercise_serializers.AdjustTrainingPlanSerializer(data=request.data)

    if not serializer.is_valid():
        return Response({"code": 400, "error": "Campos requeridos"})

    user_id = request.user.id
    result = exercise_services.adjust_training_plan(
        user_id=user_id,
        plan_id=serializer.validated_data["plan_id"],
        weekly_frequency=serializer.validated_data.get("weekly_frequency"),
        duration_weeks=serializer.validated_data.get("duration_weeks"),
    )

    if not result["success"]:
        error_message = result["message"]
        return Response({"code": _error_status_code(error_message), "error": error_message})

    output = exercise_serializers.TrainingPlanSerializer(result["data"])
    return Response({"code": 200, "data": output.serialize()})


@api_view(["POST"])
def regenerate_plan_routines(request):
    serializer = exercise_serializers.RegeneratePlanRoutinesSerializer(data=request.data)

    if not serializer.is_valid():
        return Response({"code": 400, "error": "Campos requeridos"})

    user_id = request.user.id
    result = exercise_services.regenerate_plan_routines(
        user_id=user_id,
        plan_id=serializer.validated_data["plan_id"],
    )

    if not result["success"]:
        error_message = result["message"]
        return Response({"code": _error_status_code(error_message), "error": error_message})

    output = exercise_serializers.TrainingPlanSerializer(result["data"])
    return Response({"code": 200, "data": output.serialize()})


@api_view(["GET"])
def exercise_detail(request, exercise_id):
    plan_routine_id = int(request.query_params.get("plan_routine_id"))

    detail_data = exercise_services.get_exercise_detail_service(
        user=request.user,
        exercise_id=exercise_id,
        plan_routine_id=plan_routine_id,
    )

    output = exercise_serializers.ExerciseDetailSerializer(detail_data)
    return Response({"code": 200, "data": output.serialize()}, status=status.HTTP_200_OK)


@api_view(["GET"])
def session_exercises_list(request, plan_routine_id):
    session_exercises = exercise_services.get_session_exercises_list_service(
        user=request.user,
        plan_routine_id=plan_routine_id,
    )

    output = exercise_serializers.SessionExerciseListSerializer(session_exercises)
    return Response({"code": 200, "data": output.serialize()}, status=status.HTTP_200_OK)
