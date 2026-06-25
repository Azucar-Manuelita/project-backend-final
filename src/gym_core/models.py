from django.contrib.auth.models import AbstractUser
from django.db import models


class GymUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = "gym_user"


class Goal(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        db_table = "goal"


class Limitation(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        db_table = "limitation"


class UserLimitation(models.Model):
    user = models.ForeignKey(GymUser, on_delete=models.CASCADE)
    limitation = models.ForeignKey(Limitation, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = "user_limitation"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "limitation"],
                name="unique_user_limitation",
            )
        ]


class MuscularArea(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "muscular_area"


class Machine(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "machine"


class Exercise(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    muscular_area = models.ForeignKey(MuscularArea, on_delete=models.PROTECT)
    machine = models.ForeignKey(Machine, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = "exercise"


class ExerciseLimitation(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    limitation = models.ForeignKey(Limitation, on_delete=models.CASCADE)

    class Meta:
        db_table = "exercise_limitation"
        constraints = [
            models.UniqueConstraint(
                fields=["exercise", "limitation"],
                name="unique_exercise_limitation",
            )
        ]


class Routine(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "routine"


class GoalRoutine(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE)

    class Meta:
        db_table = "goal_routine"
        constraints = [
            models.UniqueConstraint(
                fields=["goal", "routine"],
                name="unique_goal_routine",
            )
        ]


class RoutineExercise(models.Model):
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    series = models.PositiveIntegerField()
    repetitions = models.PositiveIntegerField()

    class Meta:
        db_table = "routine_exercise"
        constraints = [
            models.UniqueConstraint(
                fields=["routine", "exercise"],
                name="unique_routine_exercise",
            )
        ]


class TrainingPlan(models.Model):
    user = models.ForeignKey(GymUser, on_delete=models.CASCADE)
    goal = models.ForeignKey(Goal, on_delete=models.PROTECT)
    weekly_frequency = models.PositiveIntegerField()
    duration_weeks = models.PositiveIntegerField()
    start_date = models.DateField()
    status = models.CharField(max_length=100)

    class Meta:
        db_table = "training_plan"


class PlanRoutine(models.Model):
    plan = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE)
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE)
    session_number = models.PositiveIntegerField()

    class Meta:
        db_table = "plan_routine"
        constraints = [
            models.UniqueConstraint(
                fields=["plan", "routine", "session_number"],
                name="unique_plan_routine_session",
            )
        ]


class WorkoutLog(models.Model):
    plan = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE)
    routine = models.ForeignKey(Routine, on_delete=models.PROTECT)
    logged_at = models.DateTimeField()

    class Meta:
        db_table = "workout_log"


class FitnessLevel(models.Model):
    name = models.CharField(max_length=255)
    series_multiplier = models.FloatField()
    repetitions_multiplier = models.FloatField()

    class Meta:
        db_table = "fitness_level"


class UserAreaFitnessLevel(models.Model):
    user = models.ForeignKey(GymUser, on_delete=models.CASCADE)
    muscular_area = models.ForeignKey(MuscularArea, on_delete=models.CASCADE)
    fitness_level = models.ForeignKey(FitnessLevel, on_delete=models.PROTECT)

    class Meta:
        db_table = "user_area_fitness_level"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "muscular_area"],
                name="unique_user_muscular_area",
            )
        ]