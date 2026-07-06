from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from gym_core.models import GymUser

class AdminUserProfileTestCase(APITestCase):

    def setUp(self):
        # 1. Creamos un usuario Administrador (is_staff=True)
        self.admin_user = GymUser.objects.create_user(
            username="admin_tester",
            email="admin@manuelitagym.com",
            password="securepassword123",
            is_staff=True
        )

        # 2. Creamos un usuario Cliente común (is_staff=False) que servirá como objetivo de consulta
        self.target_user = GymUser.objects.create_user(
            username="juan_perez",
            email="juan.perez@gymmail.com",
            password="clientpassword123",
            is_staff=False,
            age=28,
            weight=75.2
        )

        # 3. Creamos otro usuario Cliente común para probar la denegación de accesos indeseados
        self.regular_user = GymUser.objects.create_user(
            username="usuario_normal",
            email="normal@gymmail.com",
            password="normalpassword123",
            is_staff=False
        )

        # Nombre de la ruta configurada en urls.py
        self.url_name = "admin-user-profile"

    def test_get_user_profile_as_admin_success(self):
        """Caso 1: Un administrador puede ver con éxito el perfil de un usuario registrado."""
        # Autenticamos al administrador en el cliente de pruebas
        self.client.force_authenticate(user=self.admin_user)
        
        # Generamos la URL dinámica usando el ID del usuario objetivo
        url = reverse(self.url_name, kwargs={"user_id": self.target_user.id})
        response = self.client.get(url)

        # Validaciones de la respuesta HTTP y estructura de datos establecida
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["code"], 200)
        self.assertIn("data", response.data)
        self.assertEqual(response.data["data"]["basic_data"]["username"], self.target_user.username)
        self.assertEqual(response.data["data"]["basic_data"]["email"], self.target_user.email)

    def test_get_user_profile_as_regular_user_forbidden(self):
        """Caso 2: Un usuario no administrador tiene prohibido acceder a esta ruta (403)."""
        # Autenticamos a un usuario común sin privilegios de staff
        self.client.force_authenticate(user=self.regular_user)
        
        url = reverse(self.url_name, kwargs={"user_id": self.target_user.id})
        response = self.client.get(url)

        # Validaciones del bloqueo de seguridad por rol
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["code"], 403)
        self.assertEqual(response.data["error"], "Only administrators can access this information")

    def test_get_user_profile_by_admin_user_not_found(self):
        """Caso 3: Si el usuario no existe, el manejador global retorna un 404 Not Found."""
        self.client.force_authenticate(user=self.admin_user)
        
        # Usamos un ID que sabemos perfectamente que no existe en la base de datos
        non_existent_id = 99999
        url = reverse(self.url_name, kwargs={"user_id": non_existent_id})
        response = self.client.get(url)

        # Validamos que escale la excepción ObjectDoesNotExist hacia el exception_handler global
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "El usuario solicitado no existe.")

    def test_get_user_profile_by_admin_invalid_id(self):
        """Caso 4: Si se envía un ID inválido (<= 0), el servicio responde con un error de negocio (400)."""
        self.client.force_authenticate(user=self.admin_user)
        
        # Un ID de 0 o negativo es inválido según las reglas del servicio
        invalid_id = 0
        url = reverse(self.url_name, kwargs={"user_id": invalid_id})
        response = self.client.get(url)

        # Validamos que se ejecute la restricción controlada sin excepciones rotas
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["code"], 400)
        self.assertEqual(response.data["error"], "Invalid user ID")