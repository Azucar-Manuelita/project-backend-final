from rest_framework import serializers

class User_Serializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, max_length=100, write_only=True)

class User_additional_info_serializer(serializers.Serializer):
    email = serializers.EmailField()
    age = serializers.IntegerField(required=False)
    weight = serializers.FloatField(required=False)