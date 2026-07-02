from rest_framework.decorators import api_view
from rest_framework.response import Response

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