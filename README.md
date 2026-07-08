# 🏋️ Gym Backend

Backend desarrollado en **Django** para un sistema de gestión y generación de planes de entrenamiento personalizados para usuarios de un gimnasio.

El proyecto expone una **API REST** consumida por un frontend desarrollado en Vue.js, permitiendo administrar usuarios, ejercicios, máquinas y planes de entrenamiento.

## Tecnologías

* Python
* Django
* Django REST Framework
* PostgreSQL
* Docker & Docker Compose

## Arquitectura

El proyecto sigue una arquitectura por capas para separar responsabilidades:

* **Controllers:** reciben las peticiones HTTP y gestionan las respuestas.
* **Services:** contienen la lógica de negocio del sistema.
* **Repositories:** realizan el acceso a la base de datos mediante el ORM de Django.
* **Models:** representan las entidades y relaciones de la base de datos.
* **Serializers:** validan los datos y convierten los modelos a formato JSON para la API.

La persistencia de datos se realiza sobre **PostgreSQL**, ejecutándose dentro de un contenedor Docker.

---

# Puesta en marcha

> Antes de iniciar, asegúrese de tener **Docker Desktop** en ejecución y haber clonado este repositorio.

### 1. Crear el entorno virtual

```bash
python -m venv venv
```

### 2. Activar el entorno virtual

**Windows**

```bash
.\venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### 3. Limpiar la base de datos (opcional si ya existe una instancia previa)

```bash
docker compose down -v
```

### 4. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 5. Iniciar PostgreSQL con Docker

```bash
docker compose up -d
```

### 6. Generar las migraciones

```bash
python manage.py makemigrations
```

### 7. Aplicar las migraciones

```bash
python manage.py migrate
```

### 8. Cargar los datos iniciales

```bash
python manage.py seed_db
```

### 9. Ejecutar el servidor

```bash
python manage.py runserver
```

El servidor estará disponible en:

```text
http://127.0.0.1:8000/
```
