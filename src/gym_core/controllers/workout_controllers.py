from rest_framework.decorators import api_view
from rest_framework.response import Response

from gym_core.services import workout_services
from gym_core.serializers import workout_serializers


@api_view(["GET"])
def get_current_workout_plan(request):

    user_id = request.user.id

    plan_data = workout_services.get_current_workout_plan(user_id)

    serializer = workout_serializers.WorkoutPlanSerializer(plan_data)
    return Response({"code": 200, "data": serializer.serialize()})