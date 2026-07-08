from rest_framework.decorators import api_view
from rest_framework.response import Response
import gym_core.serializers.user_serializers as serializers
import gym_core.services.auth_services as auth_services

@api_view(['POST'])
def create_user(request):
    serializer = serializers.UserSerializer(data=request.data)

    if serializer.is_valid():
        result = auth_services.register_user(serializer.validated_data['email'], serializer.validated_data['username'], serializer.validated_data['password'])
        print('Resultado del registro de usuario:', result)        
        if result['success']:
            return Response({"code": 201, "message": "Usuario creado exitosamente", "token": result['token']})
        else:
            return Response({"code": 400, "error": result['message']})
    else:
        return Response({"code": 400, "error": "Campos requeridos"})
    
@api_view(['POST'])
def login(request):
    serializer = serializers.UserLoginSerializer(data=request.data)

    if serializer.is_valid():
        result = auth_services.authenticate_user(serializer.validated_data['username'], serializer.validated_data['password'])
        if result['success']:
            return Response({"code": 200, "message": "Autenticacion exitosa", "token": result['token'], "staff": result['staff']})
        else:
            return Response({"code": 401, "error": result['message']})
    else:
        return Response({"code": 400, "error": "Campos requeridos"})