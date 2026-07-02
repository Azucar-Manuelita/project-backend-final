from rest_framework.views import exception_handler
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status

def global_exception_handler(exc, context):
    
    response = exception_handler(exc, context)

    if response is None and isinstance(exc, ObjectDoesNotExist):
        return Response(
            {"detail": "El plan activo solicitado no existe."},
            status=status.HTTP_404_NOT_FOUND
        )

    return response