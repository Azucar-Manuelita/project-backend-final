from rest_framework import serializers

def no_invalid_chars(name: str) -> bool:
    invalid_chars = set('!@#$%^&*()+=[]{}|\\;:"<>,.?/')
    return len(invalid_chars.intersection(name)) == 0

class exercise_serializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=500)
    area = serializers.ChoiceField(choices=["Brazos", "Pecho", "Espalda", "Abdomen", "Piernas", "Cardio"])
    machine = serializers.CharField(max_length=50)

    def validate_name(self, value):
        if not no_invalid_chars(value):
            raise serializers.ValidationError("El nombre contiene caracteres inválidos.")
        return value

class machine_serializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)

    def validate_name(self, value):
        if not no_invalid_chars(value):
            raise serializers.ValidationError("El nombre contiene caracteres inválidos.")
        return value
    

class exercise_response_serializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
    area = serializers.CharField(source='muscular_area.name') 
    machine = serializers.CharField(source='machine.name')