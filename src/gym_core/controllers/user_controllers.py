from rest_framework.decorators import api_view
from rest_framework.response import Response
import gym_core.serializers.user_serializers as serializers
import gym_core.services.user_services as user_services
import gym_core.services.auth_services as auth_services



@api_view(['POST'])
def update_user_info(request):
    serializer=serializers.User_additional_info_serializer(data=request.data)

    if serializer.is_valid():
        user=user_services.search_user(serializer.validated_data['username'])
        if user['success']:
            result=user_services.update_user_info(serializer.validated_data.get('age'), serializer.validated_data.get('weight'), user['user'])
            if result['success']:
                return Response({"code":200,"message":result['message']})
        return Response({"code":404,"error":user['message']})