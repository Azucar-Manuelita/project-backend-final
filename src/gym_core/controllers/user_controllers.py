from rest_framework.decorators import api_view
from rest_framework.response import Response
import gym_core.serializers.user_serializers as serializers
import gym_core.services.user_services as user_services
import gym_core.services.auth_services as auth_services


@api_view(['GET'])
def show_initial_training_data(request):
    limitations=user_services.show_limitations()
    areas=user_services.show_areas()
    if not limitations['success']:
        return Response({"code":404,"error":limitations['message']})
    if not areas['success']:
        return Response({"code":404,"error":areas['message']})
    return Response({"code":200,"limitations":limitations['message'], "areas":areas['message']})

@api_view(['GET'])
def latest_user_training_data(request):
    user = user_services.show_last_training_data(request.headers.get('Token'))
    if user['success']:
        return Response({"code": 200, "data": user['data']})
    return Response({"code": 404, "error": user['error']})
    
@api_view(['POST'])
def update_user_training_data(request):
    age = request.data.get('age')
    weight = request.data.get('weight')
    limitations = request.data.get('limitations', [])
    areas = request.data.get('areas', [])

    serializer = serializers.UserProfileUpdateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({"code": 400, "error": serializer.errors})

    user = user_services.token_to_user(request.headers.get('Token'))

    if not user['success']:
        return Response({"code": 404, "error": user['message']})

    result = user_services.update_user_info(user['user'], weight, age, limitations, areas)

    if result['success']:
        return Response({"code": 200, "message": result['message']})
    return Response({"code": 400})


from gym_core.services import user_services
from gym_core.serializers import user_serializers


@api_view(["GET"])
def get_user_profile(request):

    user_id = request.user.id

    result = user_services.get_user_profile_service(user_id)

    if not result["success"]:
        error_message = result["message"]
        status_code = 404 if "not found" in error_message.lower() else 400
        return Response({"code": status_code, "error": error_message})

    serializer = user_serializers.UserProfileSerializer(result["data"])
    return Response({"code": 200, "data": serializer.serialize()})


@api_view(["GET"])
def get_user_profile_by_admin(request, user_id: int):

    if not request.user.is_staff:
        return Response(
            {"code": 403, "error": "Only administrators can access this information"},
            status=403,
        )

    result = user_services.get_user_profile_by_admin_service(user_id)

    if not result["success"]:
        return Response({"code": 400, "error": result["message"]}, status=400)

    serializer = user_serializers.UserProfileSerializer(result["data"])
    return Response({"code": 200, "data": serializer.serialize()})

@api_view(["GET"])
def get_users_list_by_admin(request):

    if not request.user.is_staff:
        return Response(
            {"code": 403, "error": "Only administrators can view the user database"},
            status=403,
        )

    result = user_services.get_all_users_summary_service()

    return Response({"code": 200, "data": result["data"]})