from rest_framework import serializers

class User_Serializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100, write_only=True)

class User_login_serializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100, write_only=True)