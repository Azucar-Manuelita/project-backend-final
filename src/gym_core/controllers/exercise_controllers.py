from rest_framework.decorators import api_view
from rest_framework.response import Response

from gym_core.services import exercise_services
from gym_core.serializers import exercise_serializers

@api_view(['POST'])
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