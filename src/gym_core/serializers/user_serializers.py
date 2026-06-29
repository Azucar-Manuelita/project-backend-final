from rest_framework import serializers

class User_Serializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100, write_only=True)

class User_login_serializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100, write_only=True)


class UserProfileSerializer:


    def __init__(self, profile_data: dict):
        self._data = profile_data

    def serialize(self) -> dict:

        return {
            "basic_data": self._build_basic_data(),
            "training_goals": self._build_training_goals(),
            "physical_test_results": self._build_physical_test_results(),
            "training_period": self._build_training_period(),
            "physical_limitations": self._build_physical_limitations(),
        }

    def _build_basic_data(self) -> dict:
        return {
            "username": self._data.get("username", "PENDING"),
            "role": "ACTIVE MEMBER",
            "email": self._data.get("email", "PENDING"),
            "age": self._data.get("age") if self._data.get("age") is not None else "PENDING",
            "weight": self._data.get("weight") if self._data.get("weight") is not None else "PENDING",
        }

    def _build_training_goals(self) -> dict:
        primary = self._data.get("primary_goal") or "PENDING"
        secondary = self._data.get("secondary_goal") or "PENDING"
        return {
            "primary": primary,
            "secondary": secondary,
        }

    def _build_physical_test_results(self) -> dict:

        areas = self._data.get("physical_test_areas", [])

        if not areas:
            return {
                "areas": [
                    {
                        "muscular_area": "PENDING",
                        "fitness_level": "PENDING",
                    }
                ]
            }

        return {"areas": areas}

    def _build_training_period(self) -> dict:

        days_per_week = self._data.get("days_per_week")
        duration_weeks = self._data.get("duration_weeks")

        formatted_days = (
            f"{days_per_week} DAYS PER WEEK" if days_per_week is not None else "PENDING"
        )
        formatted_duration = (
            f"{duration_weeks} WEEKS" if duration_weeks is not None else "PENDING"
        )

        return {
            "days_per_week": formatted_days,
            "duration_weeks": formatted_duration,
        }

    def _build_physical_limitations(self) -> list:

        limitations = self._data.get("physical_limitations", [])

        if not limitations:
            return [{"name": "PENDING", "notes": "Not specified"}]

        return [
            {
                "name": lim.get("name", "PENDING"),
                "notes": lim.get("notes") or "Not specified",
            }
            for lim in limitations
        ]