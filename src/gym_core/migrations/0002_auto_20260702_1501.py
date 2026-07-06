from django.db import migrations

def seed_data(apps, schema_editor):
    MuscularArea = apps.get_model("gym_core", "MuscularArea")

    areas = [
        "Brazos",
        "Pecho",
        "Espalda",
        "Abdomen",
        "Piernas",
        "Cardio"
    ]

    for area in areas:
        MuscularArea.objects.get_or_create(name=area)

class Migration(migrations.Migration):

    dependencies = [
        ("gym_core", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_data),
    ]