from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from gym_core.services import exercise_services
from gym_core.serializers import exercise_serializers

@api_view(['POST'])
#@permission_classes([IsAdminUser])
def create_exercise(request):
    serializer = exercise_serializers.exercise_serializer(data=request.data)
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
#@permission_classes([IsAdminUser])
def create_machine(request):
    serializer = exercise_serializers.machine_serializer(data=request.data)
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
    serializer = exercise_serializers.exercise_response_serializer(exercises, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_machines(request):
    machines = exercise_services.get_machines()
    serializer = exercise_serializers.machine_serializer(machines, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_exercises(request):
    exercises = exercise_services.get_exercises()
    serializer = exercise_serializers.exercise_response_serializer(exercises, many=True)
    return Response(serializer.data)