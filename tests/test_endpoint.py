import os
import sys
import django
from django.test import Client

# 1. Le decimos a Python que incluya la carpeta "src" en su búsqueda de módulos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, "src"))

# 2. Configurar el entorno de Django (asegúrate de que "config.settings" es tu ruta real)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings") 
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.get(username="testuser")

# Inicializar el cliente de pruebas de Django que simula Postman
client = Client()

# Forzar la autenticación del usuario en la sesión simulada
client.force_login(user)

print("--- PROBANDO ESCENARIO 1: USUARIO CON PLAN ACTIVO (Debe dar 200 y 33.33% de progreso) ---")
response = client.get("/gym_app/api/workouts/current/", HTTP_ACCEPT="application/json")
print(f"Código de Estado: {response.status_code}")
print("JSON Recibido:")
import json
print(json.dumps(response.json(), indent=4, ensure_ascii=False))


print("\n--- PROBANDO ESCENARIO 2: MANEJADOR GLOBAL DE EXCEPCIONES (Debe dar 404) ---")
# Creamos otro usuario que no tiene ningún plan asignado
otro_usuario, _ = User.objects.get_or_create(username="sinplan")
client.force_login(otro_usuario)

response_404 = client.get("/gym_app/api/workouts/current/", HTTP_ACCEPT="application/json")
print(f"Código de Estado: {response_404.status_code}")
print("JSON Recibido de Error:")
print(json.dumps(response_404.json(), indent=4, ensure_ascii=False))