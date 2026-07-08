class WorkoutSessionSerializer:

    def __init__(self, session_data: dict):
        self._data = session_data

    def serialize(self) -> dict:
        return {
            "plan_routine_id": self._data.get("plan_routine_id"),
            "session_number": self._data.get("session_number"),
            "routine_name": self._data.get("routine_name"),
            "is_completed": self._data.get("is_completed", False),
        }


class WorkoutPlanSerializer:

    def __init__(self, plan_data: dict):
        self._data = plan_data

    def serialize(self) -> dict:
        return {
            "plan_header": self._build_plan_header(),
            "sessions": self._build_sessions(),
        }

    def _build_plan_header(self) -> dict:
        return {
            "goal": self._data.get("goal", "PENDING"),
            "weekly_frequency": self._data.get("weekly_frequency"),
            "duration_weeks": self._data.get("duration_weeks"),
            "progress_percentage": self._data.get("progress_percentage", 0.0),
        }

    def _build_sessions(self) -> list:
        sessions = self._data.get("sessions", [])
        return [WorkoutSessionSerializer(session).serialize() for session in sessions]


class SessionCompletionSerializer:

    def __init__(self, completion_data: dict):
        self._data = completion_data

    def serialize(self) -> dict:
        return {
            "plan_routine_id": self._data.get("plan_routine_id"),
            "is_completed": self._data.get("is_completed", False),
        }