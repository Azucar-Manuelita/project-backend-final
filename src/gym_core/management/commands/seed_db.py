from datetime import date
from unicodedata import normalize

from django.core.management.base import BaseCommand

from gym_core import models
from gym_core.repositories.user_repository import get_user_by_correo
from gym_core.services.auth_services import register_user


class Command(BaseCommand):
    help = 'Popula la base de datos con datos de prueba estables'

    def _normalize_name(self, value):
        if not value:
            return ""
        normalized = normalize("NFKD", str(value))
        ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
        return "".join(char.lower() for char in ascii_value if char.isalnum())

    def _normalize_text(self, value):
        if value is None:
            return None
        if not isinstance(value, str):
            return value
        replacements = str.maketrans({
            "á": "a",
            "é": "e",
            "í": "i",
            "ó": "o",
            "ú": "u",
            "Á": "A",
            "É": "E",
            "Í": "I",
            "Ó": "O",
            "Ú": "U",
            "ñ": "n",
            "Ñ": "N",
            "¡": "",
            "!": "",
            "¿": "",
            "?": "",
            "“": "",
            "”": "",
            "“": "",
            "'": "",
            '"': "",
        })
        return value.translate(replacements)

    def _sanitize_payload(self, payload):
        if not isinstance(payload, dict):
            return payload
        sanitized = {}
        for key, value in payload.items():
            if isinstance(value, str):
                sanitized[key] = self._normalize_text(value)
            else:
                sanitized[key] = value
        return sanitized

    def _get_or_create_named(self, model_class, name, defaults=None):
        defaults = defaults or {}
        defaults = self._sanitize_payload(defaults)
        normalized_name = self._normalize_name(name)
        existing = next(
            (
                obj
                for obj in model_class.objects.all()
                if self._normalize_name(getattr(obj, "name", "")) == normalized_name
            ),
            None,
        )
        if existing is not None:
            return existing, False
        return model_class.objects.get_or_create(name=self._normalize_text(name), defaults=defaults)

    def _get_named(self, model_class, name):
        normalized_name = self._normalize_name(name)
        return next(
            (
                obj
                for obj in model_class.objects.all()
                if self._normalize_name(getattr(obj, "name", "")) == normalized_name
            ),
            None,
        )

    def handle(self, *args, **kwargs):
        self.stdout.write("Sembrando base de datos...")

        goals_data = [
            {
                "name": "Perdida de Grasa",
                "description": "Enfocado en deficit calorico y entrenamientos metabolicos para reducir el porcentaje de grasa corporal."
            },
            {
                "name": "Hipertrofia Muscular",
                "description": "Disenado para aumentar la masa muscular mediante entrenamiento de fuerza con cargas progresivas y volumen adecuado."
            },
            {
                "name": "Resistencia Cardiovascular",
                "description": "Centrado en mejorar la capacidad pulmonar y cardiaca a traves de ejercicios aerobicos de larga duracion o alta intensidad."
            },
            {
                "name": "Fuerza Maxima",
                "description": "Orientado a levantar el mayor peso posible a bajas repeticiones, mejorando el reclutamiento del sistema nervioso y muscular."
            },
            {
                "name": "Tonificacion y Definicion",
                "description": "Combina el mantenimiento de la masa muscular existente con una leve perdida de grasa para resaltar las formas del cuerpo."
            },
            {
                "name": "Flexibilidad y Movilidad",
                "description": "Enfocado en estiramientos y ejercicios articulares para mejorar el rango de movimiento, prevenir lesiones y aliviar la rigidez."
            },
            {
                "name": "Acondicionamiento Fisico General",
                "description": "Ideal para principiantes que buscan salir del sedentarismo, combinando fuerza, cardio y coordinacion basica."
            },
            {
                "name": "Potencia y Atletismo",
                "description": "Dirigido a deportistas que buscan mejorar su velocidad, saltos y movimientos explosivos mediante ejercicios pliometricos y olimpicos."
            }
        ]

        limitations = [
            {
                "name": "Lesion Lumbar / Hernia Discal",
                "description": "Restriccion en ejercicios de alta carga axial sobre la columna (como sentadillas pesadas o peso muerto) y enfasis en fortalecimiento del core."
            },
            {
                "name": "Hipertension Arterial",
                "description": "Requiere control de la intensidad, evitacion de la maniobra de Valsalva prolongada y transiciones lentas al cambiar de posturas."
            },
            {
                "name": "Condromalacia Rotuliana / Dolor de Rodilla",
                "description": "Limitacion en rangos profundos de flexion de rodilla con carga estresante y enfoque en el fortalecimiento de cuadriceps e isquiotibiales."
            },
            {
                "name": "Sindrome del Tunel Carpiano",
                "description": "Dificultad o dolor en ejercicios que requieran un agarre excesivamente pesado o hiperextension prolongada de las munecas."
            },
            {
                "name": "Lesion de Manguito Rotador",
                "description": "Restriccion en movimientos de empuje o traccion por encima de la cabeza y ejercicios que fuercen la rotacion interna/externa del hombro con carga."
            },
            {
                "name": "Asma / Capacidad Respiratoria Reducida",
                "description": "Necesidad de tiempos de recuperacion mas prolongados entre series y monitoreo constante de la intensidad cardiovascular."
            },
            {
                "name": "Artrosis / Desgaste Articular",
                "description": "Evita ejercicios de alto impacto (saltos, carrera) priorizando entrenamientos en maquinas guiadas, natacion o el uso de eliptica."
            },
            {
                "name": "Diabetes (Tipo 1 o 2)",
                "description": "Monitoreo del gasto calorico y control estricto de la intensidad para prevenir episodios de hipoglucemia durante o despues del entrenamiento."
            }
        ]

        # Estas son las 6 áreas musculares oficiales de la app (las mismas que
        # siembra la migración 0002_auto_20260702_1501). No se agregan más:
        # cualquier área adicional aquí generaría duplicados/conflictos con
        # el resto del sistema (validación de ejercicios, clasificación de
        # usuarios, etc.), que solo reconoce estas 6.
        areas = [
            { "name": "Brazos" },
            { "name": "Pecho" },
            { "name": "Espalda" },
            { "name": "Abdomen" },
            { "name": "Piernas" },
            { "name": "Cardio" }
        ]

        machines = [
            { "name": "Prensa de Piernas (Leg Press)" },
            { "name": "Extension de Cuadriceps en Maquina" },
            { "name": "Curl de Pierna Sentado (Leg Curl)" },
            { "name": "Curl de Pierna Acostado (Lying Leg Curl)" },
            { "name": "Maquina de Abductores / Adductores" },
            { "name": "Maquina de Elevacion de Pantorrillas (Calf Raise)" },
            { "name": "Maquina de Sentadilla Hack (Hack Squat)" },
            { "name": "Polea Alta (Lat Pulldown)" },
            { "name": "Maquina de Remo Sentado con Cable (Seated Row)" },
            { "name": "Maquina de Pec Deck / Aperturas de Pecho" },
            { "name": "Press de Pecho en Maquina Hammer Strength" },
            { "name": "Press de Hombros en Maquina" },
            { "name": "Maquina de Elevaciones Laterales" },
            { "name": "Polea Cruzada / Cruce de Poleas (Cable Crossover)" },
            { "name": "Maquina de Fondos / Dominadas Asistidas" },
            { "name": "Predicador en Maquina para Biceps" },
            { "name": "Maquina de Extension de Triceps" },
            { "name": "Maquina de Crunch Abdominal" },
            { "name": "Banco de Hiperextensiones" },
            { "name": "Jaula de Sentadillas / Rack de Potencia" },
            { "name": "Maquina Smith (Multicadena / Multipower)" },
            { "name": "Banco Plano para Press de Banca" },
            { "name": "Banco Inclinado para Press de Banca" },
            { "name": "Cinta de Correr (Treadmill)" },
            { "name": "Bicicleta Estatica / Spinning" },
            { "name": "Bicicleta Air Bike (Assault Bike)" },
            { "name": "Maquina Eliptica" },
            { "name": "Maquina de Escaladora (Stairmaster)" },
            { "name": "Maquina de Remo de Aire (Rowing Machine)" },
            { "name": "Mancuernas" },
            { "name": "Barra Olimpica" },
            { "name": "Polea Baja" },
            { "name": "Banco Declinado para Press de Banca" },
        ]

        routines = [
            { "name": "Circuito Metabólico de Alta Intensidad (HIIT)" },
            { "name": "Rutina de Fuerza y Resistencia (Cardio-Fuerza)" },
            { "name": "Entrenamiento de Déficit Adaptativo (Full Body)" },
            { "name": "Rutina Push / Pull / Legs (Empuje, Tracción, Pierna)" },
            { "name": "Rutina Torso / Pierna de Alta Frecuencia" },
            { "name": "Entrenamiento de Volumen Alemán (GVT)" },
            { "name": "Rutina de Resistencia Aeróbica en Estado Estacionario (LISS)" },
            { "name": "Intervalos de Potencia y Capacidad Anaeróbica" },
            { "name": "Circuito AMRAP de Resistencia General" },
            { "name": "Rutina de Fuerza Máxima 5x5 (Madcow / Stronglifts)" },
            { "name": "Bloque de Intensidad y Sobrecarga Progresiva Peaking" },
            { "name": "Rutina de Fuerza Estricta Basada en RPE" },
            { "name": "Rutina de Recomposición Corporal ABC" },
            { "name": "Circuito de Densidad con Súper-Series" },
            { "name": "Entrenamiento Escuplido con Énfasis Estético" },
            { "name": "Rutina de Descompresión Lumbar y Core" },
            { "name": "Sesión de Flexibilidad Dinámica y Apertura de Cadera" },
            { "name": "Rutina de Movilidad Articular para Levantadores" },
            { "name": "Rutina de Iniciación y Adaptación Anatómica" },
            { "name": "Full Body de Circuitos Cardiovasculares Ligeros" },
            { "name": "Rutina de Coordinación y Tonificación Básica" },
            { "name": "Entrenamiento Pliométrico y de Elasticidad Muscular" },
            { "name": "Rutina de Potencia con Derivados Olímpicos" },
            { "name": "Preparación Física General de Agilidad y Esprint" }
        ]

        # Solo 3 niveles de condición física (coincide con lo que ya espera
        # el frontend: ver FITNESS_LEVELS en ProfileView.vue). No agregar
        # más niveles: el catálogo que ve el usuario en el onboarding y en
        # "Mi Perfil" sale directamente de esta tabla.
        fitness_levels = [
            {
                "name": "Principiante",
                "series_multiplier": 1.0,
                "repetitions_multiplier": 1.0
            },
            {
                "name": "Intermedio",
                "series_multiplier": 1.3,
                "repetitions_multiplier": 1.3
            },
            {
                "name": "Avanzado",
                "series_multiplier": 1.6,
                "repetitions_multiplier": 1.6
            }
        ]

        exercises_data = [
            {
                "name": "Press de Banca Plano",
                "description": "Ejercicio multiarticular básico para desarrollar la fuerza y masa muscular del pectoral mayor.",
                "muscle_area": "Pecho",
                "machine": "Banco Plano para Press de Banca"
            },
            {
                "name": "Aperturas en Pec Deck",
                "description": "Movimiento de aislamiento ideal para buscar una contracción máxima en la parte interna del pecho.",
                "muscle_area": "Pecho",
                "machine": "Máquina de Pec Deck / Aperturas de Pecho"
            },
            {
                "name": "Cruce de Poleas Altas",
                "description": "Enfocado en trabajar la parte inferior y externa del pectoral mediante una aducción constante.",
                "muscle_area": "Pecho",
                "machine": "Polea Cruzada / Cruce de Poleas (Cable Crossover)"
            },
            {
                "name": "Jalón al Pecho",
                "description": "Ejercicio fundamental para trabajar la amplitud de la espalda, principalmente el dorsal ancho.",
                "muscle_area": "Espalda",
                "machine": "Polea Alta (Lat Pulldown)"
            },
            {
                "name": "Remo Sentado con Cable",
                "description": "Trabaja el grosor de la espalda media, los romboides y la sección baja del trapecio.",
                "muscle_area": "Espalda",
                "machine": "Máquina de Remo Sentado con Cable (Seated Row)"
            },
            {
                "name": "Remo en Máquina de Aire",
                "description": "Excelente para resistencia muscular en la espalda y acondicionamiento general.",
                "muscle_area": "Espalda",
                "machine": "Máquina de Remo de Aire (Rowing Machine)"
            },
            {
                "name": "Press de Hombros en Máquina",
                "description": "Movimiento compuesto enfocado en el deltoides anterior con una trayectoria guiada y segura.",
                "muscle_area": "Pecho",
                "machine": "Press de Hombros en Máquina"
            },
            {
                "name": "Elevaciones Laterales en Máquina",
                "description": "Aislamiento estricto del deltoides lateral para dar un aspecto más ancho a los hombros.",
                "muscle_area": "Pecho",
                "machine": "Máquina de Elevaciones Laterales"
            },
            {
                "name": "Vuelos Posteriores en Pec Deck",
                "description": "Sentándose a la inversa en la máquina, aísla el deltoides posterior de forma muy eficiente.",
                "muscle_area": "Pecho",
                "machine": "Máquina de Pec Deck / Aperturas de Pecho"
            },
            {
                "name": "Curl en Banco Predicador",
                "description": "Aísla la cabeza corta del bíceps limitando por completo el balanceo del cuerpo.",
                "muscle_area": "Brazos",
                "machine": "Predicador en Máquina para Bíceps"
            },
            {
                "name": "Curl de Bíceps con Mancuernas",
                "description": "Ejercicio libre clásico para trabajar la fuerza y supinación de los brazos de forma unilateral.",
                "muscle_area": "Brazos",
                "machine": "Mancuernas"
            },
            {
                "name": "Curl en Polea Baja",
                "description": "Mantiene una tensión mecánica constante durante todo el rango de movimiento del ejercicio.",
                "muscle_area": "Brazos",
                "machine": "Polea Baja"
            },
            {
                "name": "Extensión de Tríceps en Polea",
                "description": "Enfocado en la cabeza lateral y medial del tríceps usando una trayectoria vertical limpia.",
                "muscle_area": "Brazos",
                "machine": "Polea Alta (Lat Pulldown)"
            },
            {
                "name": "Extensión en Máquina de Tríceps",
                "description": "Movimiento sentado que estabiliza la espalda permitiendo empujar cargas controladas.",
                "muscle_area": "Brazos",
                "machine": "Máquina de Extensión de Tríceps"
            },
            {
                "name": "Fondos Asistidos para Tríceps",
                "description": "Trabaja la fuerza de empuje de los brazos quitando un porcentaje de tu peso corporal.",
                "muscle_area": "Brazos",
                "machine": "Máquina de Fondos / Dominadas Asistidas"
            },
            {
                "name": "Curl de Antebrazo Supinado",
                "description": "Fortalece los flexores del antebrazo apoyando los brazos sobre un banco firme.",
                "muscle_area": "Brazos",
                "machine": "Barra Olímpica"
            },
            {
                "name": "Curl Inverso con Mancuernas",
                "description": "Trabaja principalmente el músculo braquiorradial situado en la zona externa del antebrazo.",
                "muscle_area": "Brazos",
                "machine": "Mancuernas"
            },
            {
                "name": "Paseo del Granjero con Mancuernas",
                "description": "Caminar sosteniendo cargas pesadas a los lados; excelente para la fuerza de agarre estática.",
                "muscle_area": "Brazos",
                "machine": "Mancuernas"
            },
            {
                "name": "Crunch Abdominal en Máquina",
                "description": "Permite añadir resistencia progresiva mediante placas al movimiento de flexión del torso.",
                "muscle_area": "Abdomen",
                "machine": "Máquina de Crunch Abdominal"
            },
            {
                "name": "Elevaciones de Piernas Colgado",
                "description": "Enfocado en la porción inferior del abdomen usando el soporte superior del rack.",
                "muscle_area": "Abdomen",
                "machine": "Jaula de Sentadillas / Rack de Potencia"
            },
            {
                "name": "Leñador en Polea Media",
                "description": "Trabaja los músculos oblicuos mediante un movimiento de rotación controlada del core.",
                "muscle_area": "Abdomen",
                "machine": "Polea Cruzada / Cruce de Poleas (Cable Crossover)"
            },
            {
                "name": "Extensión de Cuádriceps",
                "description": "Ejercicio analítico ideal para aislar el cuádriceps de forma segura sin involucrar la cadera.",
                "muscle_area": "Piernas",
                "machine": "Extensión de Cuádriceps en Máquina"
            },
            {
                "name": "Prensa de Piernas inclinada",
                "description": "Permite mover cargas altas para el desarrollo global de las piernas disminuyendo la tensión lumbar.",
                "muscle_area": "Piernas",
                "machine": "Prensa de Piernas (Leg Press)"
            },
            {
                "name": "Sentadilla Hack",
                "description": "Variante guiada de sentadilla que enfatiza la estimulación profunda de los cuádriceps.",
                "muscle_area": "Piernas",
                "machine": "Máquina de Sentadilla Hack (Hack Squat)"
            },
            {
                "name": "Curl de Pierna Sentado",
                "description": "Aísla e involucra fuertemente la musculatura isquiotibial en una posición cómoda para las rodillas.",
                "muscle_area": "Piernas",
                "machine": "Curl de Pierna Sentado (Leg Curl)"
            },
            {
                "name": "Curl de Pierna Acostado",
                "description": "Estimula los femorales en su posición más estirada gracias a la inclinación del banco.",
                "muscle_area": "Piernas",
                "machine": "Curl de Pierna Acostado (Lying Leg Curl)"
            },
            {
                "name": "Peso Muerto Rumano en Máquina Smith",
                "description": "Excelente para trabajar el estiramiento de los isquiotibiales controlando perfectamente la barra.",
                "muscle_area": "Piernas",
                "machine": "Máquina Smith (Multicadena / Multipower)"
            },
            {
                "name": "Patada de Glúteo en Polea Baja",
                "description": "Ejercicio enfocado en la extensión de cadera aislada para activar las fibras del glúteo mayor.",
                "muscle_area": "Piernas",
                "machine": "Polea Baja"
            },
            {
                "name": "Aducción de Cadera en Máquina",
                "description": "Trabaja de manera específica los músculos abductores y el glúteo medio en su fase excéntrica.",
                "muscle_area": "Piernas",
                "machine": "Máquina de Abductores / Adductores"
            },
            {
                "name": "Zancadas con Mancuernas",
                "description": "Excelente ejercicio unilateral enfocado firmemente en la cadena posterior y el glúteo.",
                "muscle_area": "Piernas",
                "machine": "Mancuernas"
            },
            {
                "name": "Elevación de Pantorrillas Sentado",
                "description": "Aísla el músculo sóleo de la pantorrilla flexionando las rodillas a 90 grados.",
                "muscle_area": "Piernas",
                "machine": "Máquina de Elevación de Pantorrillas (Calf Raise)"
            },
            {
                "name": "Elevación de Pantorrillas en Prensa",
                "description": "Permite trabajar el músculo gastrocnemio extendiendo completamente el tobillo con la pierna recta.",
                "muscle_area": "Piernas",
                "machine": "Prensa de Piernas (Leg Press)"
            },
            {
                "name": "Elevación de Talón de Pie en Smith",
                "description": "Utiliza la barra guiada para añadir peso controlado sobre los hombros al elevar los talones.",
                "muscle_area": "Piernas",
                "machine": "Máquina Smith (Multicadena / Multipower)"
            },
            {
                "name": "Encojamientos de Hombros con Barra",
                "description": "Enfocado únicamente en la elevación escapular para desarrollar la parte superior del trapecio.",
                "muscle_area": "Espalda",
                "machine": "Barra Olímpica"
            },
            {
                "name": "Encojamientos con Mancuernas",
                "description": "Permite una posición de agarre más natural a los costados del cuerpo para trabajar el trapecio.",
                "muscle_area": "Espalda",
                "machine": "Mancuernas"
            },
            {
                "name": "Remo al Mentón en Polea Baja",
                "description": "Involucra tanto las fibras medias y superiores del trapecio como los deltoides.",
                "muscle_area": "Espalda",
                "machine": "Polea Baja"
            },
            {
                "name": "Carrera en Cinta de Correr",
                "description": "Ejercicio cardiovascular de alta intensidad enfocado en mejorar la resistencia aeróbica y el consumo calórico.",
                "muscle_area": "Cardio", # Adaptado al catálogo (estímulo en tren inferior)
                "machine": "Cinta de Correr (Treadmill)"
            },
            {
                "name": "Ciclismo en Bicicleta Estática",
                "description": "Entrenamiento cardiovascular de bajo impacto ideal para el acondicionamiento aeróbico y el fortalecimiento de cuádriceps.",
                "muscle_area": "Cardio", # Adaptado al catálogo
                "machine": "Bicicleta Estática / Spinning"
            },
            {
                "name": "Caminata / Carrera en Cinta",
                "description": "Actividad cardiovascular de intensidad moderada a variable, excelente para la resistencia general y la recuperación activa.",
                "muscle_area": "Cardio", # Adaptado al catálogo
                "machine": "Cinta de Correr (Treadmill)"
            },
            {
                "name": "Ejercicio en Máquina Elíptica",
                "description": "Movimiento fluido sin impacto articular que involucra de manera simultánea el tren superior e inferior.",
                "muscle_area": "Cardio", # Adaptado al catálogo (predominio de empuje de piernas)
                "machine": "Máquina Elíptica"
            },
            {
                "name": "Pedaleo Intenso en Air Bike",
                "description": "Ejercicio metabólico de alta resistencia que utiliza la resistencia del aire para maximizar la capacidad anaeróbica.",
                "muscle_area": "Cardio", # Adaptado al catálogo (por el empuje/tracción constante de los manubrios)
                "machine": "Bicicleta Air Bike (Assault Bike)"
            },
            {
                "name": "Escalada en Máquina de Escaladora",
                "description": "Trabajo cardiovascular vertical continuo que enfatiza la potencia y resistencia de glúteos y pantorrillas.",
                "muscle_area": "Cardio", # Adaptado al catálogo
                "machine": "Máquina de Escaladora (Stairmaster)"
            },
            {
                "name": "Extensión Lumbar en Banco",
                "description": "Aislamiento centrado en el fortalecimiento de los erectores espinales, la zona baja de la espalda y los glúteos.",
                "muscle_area": "Espalda", # Adaptado al catálogo (corresponde a la cadena posterior/espalda)
                "machine": "Banco de Hiperextensiones"
            }
        ]

        exercise_limitation = [
            {
                "limitation": "Lesión Lumbar / Hernia Discal",
                "exercise": "Prensa de Piernas inclinada"
            },
            {
                "limitation": "Lesión Lumbar / Hernia Discal",
                "exercise": "Peso Muerto Rumano en Máquina Smith"
            },
            {
                "limitation": "Lesión Lumbar / Hernia Discal",
                "exercise": "Encojamientos de Hombros con Barra"
            },
            {
                "limitation": "Lesión Lumbar / Hernia Discal",
                "exercise": "Elevaciones de Piernas Colgado"
            },
            {
                "limitation": "Condromalacia Rotuliana / Dolor de Rodilla",
                "exercise": "Prensa de Piernas inclinada"
            },
            {
                "limitation": "Condromalacia Rotuliana / Dolor de Rodilla",
                "exercise": "Sentadilla Hack"
            },
            {
                "limitation": "Condromalacia Rotuliana / Dolor de Rodilla",
                "exercise": "Zancadas con Mancuernas"
            },
            {
                "limitation": "Lesión de Manguito Rotador",
                "exercise": "Press de Hombros en Máquina"
            },
            {
                "limitation": "Lesión de Manguito Rotador",
                "exercise": "Jalón al Pecho"
            },
            {
                "limitation": "Lesión de Manguito Rotador",
                "exercise": "Elevaciones de Piernas Colgado"
            },
            {
                "limitation": "Lesión de Manguito Rotador",
                "exercise": "Cruce de Poleas Altas"
            },
            {
                "limitation": "Síndrome del Túnel Carpiano",
                "exercise": "Paseo del Granjero con Mancuernas"
            },
            {
                "limitation": "Síndrome del Túnel Carpiano",
                "exercise": "Curl de Antebrazo Supinado"
            },
            {
                "limitation": "Síndrome del Túnel Carpiano",
                "exercise": "Encojamientos de Hombros con Barra"
            },
            {
                "limitation": "Síndrome del Túnel Carpiano",
                "exercise": "Press de Banca Plano"
            },
            {
                "limitation": "Artrosis / Desgaste Articular",
                "exercise": "Remo en Máquina de Aire"
            },
            {
                "limitation": "Artrosis / Desgaste Articular",
                "exercise": "Zancadas con Mancuernas"
            },
            {
                "limitation": "Asma / Capacidad Respiratoria Reducida",
                "exercise": "Remo en Máquina de Aire"
            }
        ]

        goal_routine = [
            {
                "routine": "Circuito Metabólico de Alta Intensidad (HIIT)",
                "goal": "Pérdida de Grasa"
            },
            {
                "routine": "Rutina de Fuerza y Resistencia (Cardio-Fuerza)",
                "goal": "Pérdida de Grasa"
            },
            {
                "routine": "Entrenamiento de Déficit Adaptativo (Full Body)",
                "goal": "Pérdida de Grasa"
            },
            {
                "routine": "Rutina Push / Pull / Legs (Empuje, Tracción, Pierna)",
                "goal": "Hipertrofia Muscular"
            },
            {
                "routine": "Rutina Torso / Pierna de Alta Frecuencia",
                "goal": "Hipertrofia Muscular"
            },
            {
                "routine": "Entrenamiento de Volumen Alemán (GVT)",
                "goal": "Hipertrofia Muscular"
            },
            {
                "routine": "Rutina de Resistencia Aeróbica en Estado Estacionario (LISS)",
                "goal": "Resistencia Cardiovascular"
            },
            {
                "routine": "Intervalos de Potencia y Capacidad Anaeróbica",
                "goal": "Resistencia Cardiovascular"
            },
            {
                "routine": "Circuito AMRAP de Resistencia General",
                "goal": "Resistencia Cardiovascular"
            },
            {
                "routine": "Rutina de Fuerza Máxima 5x5 (Madcow / Stronglifts)",
                "goal": "Fuerza Máxima"
            },
            {
                "routine": "Bloque de Intensidad y Sobrecarga Progresiva Peaking",
                "goal": "Fuerza Máxima"
            },
            {
                "routine": "Rutina de Fuerza Estricta Basada en RPE",
                "goal": "Fuerza Máxima"
            },
            {
                "routine": "Rutina de Recomposición Corporal ABC",
                "goal": "Tonificación y Definición"
            },
            {
                "routine": "Circuito de Densidad con Súper-Series",
                "goal": "Tonificación y Definición"
            },
            {
                "routine": "Entrenamiento Escuplido con Énfasis Estético",
                "goal": "Tonificación y Definición"
            },
            {
                "routine": "Rutina de Descompresión Lumbar y Core",
                "goal": "Flexibilidad y Movilidad"
            },
            {
                "routine": "Sesión de Flexibilidad Dinámica y Apertura de Cadera",
                "goal": "Flexibilidad y Movilidad"
            },
            {
                "routine": "Rutina de Movilidad Articular para Levantadores",
                "goal": "Flexibilidad y Movilidad"
            },
            {
                "routine": "Rutina de Iniciación y Adaptación Anatómica",
                "goal": "Acondicionamiento Físico General"
            },
            {
                "routine": "Full Body de Circuitos Cardiovasculares Ligeros",
                "goal": "Acondicionamiento Físico General"
            },
            {
                "routine": "Rutina de Coordinación y Tonificación Básica",
                "goal": "Acondicionamiento Físico General"
            },
            {
                "routine": "Entrenamiento Pliométrico y de Elasticidad Muscular",
                "goal": "Potencia y Atletismo"
            },
            {
                "routine": "Rutina de Potencia con Derivados Olímpicos",
                "goal": "Potencia y Atletismo"
            },
            {
                "routine": "Preparación Física General de Agilidad y Esprint",
                "goal": "Potencia y Atletismo"
            }
        ]

        routine_exercise = [
            #// --- PÉRDIDA DE GRASA ---
            {
                "routine": "Circuito Metabólico de Alta Intensidad (HIIT)",
                "exercise": "Remo en Máquina de Aire",
                "series": 4,
                "repetitions": 15
            },
            {
                "routine": "Circuito Metabólico de Alta Intensidad (HIIT)",
                "exercise": "Carrera en Cinta de Correr", 
                "series": 4,
                "repetitions": 1
            },
            {
                "routine": "Circuito Metabólico de Alta Intensidad (HIIT)",
                "exercise": "Leñador en Polea Media",
                "series": 3,
                "repetitions": 15
            },
            {
                "routine": "Rutina de Fuerza y Resistencia (Cardio-Fuerza)",
                "exercise": "Prensa de Piernas inclinada",
                "series": 3,
                "repetitions": 12
            },
            {
                "routine": "Rutina de Fuerza y Resistencia (Cardio-Fuerza)",
                "exercise": "Jalón al Pecho",
                "series": 3,
                "repetitions": 12
            },
            {
                "routine": "Rutina de Fuerza y Resistencia (Cardio-Fuerza)",
                "exercise": "Ciclismo en Bicicleta Estática", 
                "series": 3,
                "repetitions": 1
            },

            #// --- HIPERTROFIA MUSCULAR ---
            {
                "routine": "Rutina Push / Pull / Legs (Empuje, Tracción, Pierna)",
                "exercise": "Press de Banca Plano",
                "series": 4,
                "repetitions": 10
            },
            {
                "routine": "Rutina Push / Pull / Legs (Empuje, Tracción, Pierna)",
                "exercise": "Press de Hombros en Máquina",
                "series": 3,
                "repetitions": 10
            },
            {
                "routine": "Rutina Push / Pull / Legs (Empuje, Tracción, Pierna)",
                "exercise": "Extensión de Cuádriceps",
                "series": 4,
                "repetitions": 12
            },
            {
                "routine": "Rutina Torso / Pierna de Alta Frecuencia",
                "exercise": "Remo Sentado con Cable",
                "series": 4,
                "repetitions": 10
            },
            {
                "routine": "Rutina Torso / Pierna de Alta Frecuencia",
                "exercise": "Prensa de Piernas inclinada",
                "series": 4,
                "repetitions": 10
            },
            {
                "routine": "Rutina Torso / Pierna de Alta Frecuencia",
                "exercise": "Curl de Pierna Sentado",
                "series": 3,
                "repetitions": 12
            },

            #// --- RESISTENCIA CARDIOVASCULAR ---
            {
                "routine": "Rutina de Resistencia Aeróbica en Estado Estacionario (LISS)",
                "exercise": "Caminata / Carrera en Cinta", 
                "series": 1,
                "repetitions": 1
            },
            {
                "routine": "Rutina de Resistencia Aeróbica en Estado Estacionario (LISS)",
                "exercise": "Ejercicio en Máquina Elíptica", 
                "series": 1,
                "repetitions": 1
            },
            {
                "routine": "Intervalos de Potencia y Capacidad Anaeróbica",
                "exercise": "Pedaleo Intenso en Air Bike", 
                "series": 5,
                "repetitions": 1
            },
            {
                "routine": "Intervalos de Potencia y Capacidad Anaeróbica",
                "exercise": "Escalada en Máquina de Escaladora", 
                "series": 4,
                "repetitions": 1
            },

            #// --- FUERZA MÁXIMA ---
            {
                "routine": "Rutina de Fuerza Máxima 5x5 (Madcow / Stronglifts)",
                "exercise": "Press de Banca Plano",
                "series": 5,
                "repetitions": 5
            },
            {
                "routine": "Rutina de Fuerza Máxima 5x5 (Madcow / Stronglifts)",
                "exercise": "Peso Muerto Rumano en Máquina Smith",
                "series": 5,
                "repetitions": 5
            },
            {
                "routine": "Rutina de Fuerza Estricta Basada en RPE",
                "exercise": "Sentadilla Hack",
                "series": 4,
                "repetitions": 6
            },
            {
                "routine": "Rutina de Fuerza Estricta Basada en RPE",
                "exercise": "Encojamientos de Hombros con Barra", # Corregido usando tu catálogo de barras
                "series": 3,
                "repetitions": 6
            },

            #// --- TONIFICACIÓN Y DEFINICIÓN ---
            {
                "routine": "Rutina de Recomposición Corporal ABC",
                "exercise": "Aperturas en Pec Deck",
                "series": 3,
                "repetitions": 12
            },
            {
                "routine": "Rutina de Recomposición Corporal ABC",
                "exercise": "Zancadas con Mancuernas",
                "series": 3,
                "repetitions": 12
            },
            {
                "routine": "Rutina de Recomposición Corporal ABC",
                "exercise": "Curl de Bíceps con Mancuernas",
                "series": 3,
                "repetitions": 12
            },
            {
                "routine": "Circuito de Densidad con Súper-Series",
                "exercise": "Cruce de Poleas Altas",
                "series": 4,
                "repetitions": 15
            },
            {
                "routine": "Circuito de Densidad con Súper-Series",
                "exercise": "Extensión de Tríceps en Polea",
                "series": 4,
                "repetitions": 15
            },

            #// --- FLEXIBILIDAD Y MOVILIDAD ---
            {
                "routine": "Rutina de Descompresión Lumbar y Core",
                "exercise": "Extensión Lumbar en Banco", 
                "series": 3,
                "repetitions": 10
            },
            {
                "routine": "Rutina de Descompresión Lumbar y Core",
                "exercise": "Crunch Abdominal en Máquina",
                "series": 3,
                "repetitions": 12
            },
            {
                "routine": "Rutina de Movilidad Articular para Levantadores",
                "exercise": "Elevaciones Laterales en Máquina",
                "series": 2,
                "repetitions": 15
            },

            #// --- ACONDICIONAMIENTO FÍSICO GENERAL ---
            {
                "routine": "Rutina de Iniciación y Adaptación Anatómica",
                "exercise": "Extensión de Cuádriceps",
                "series": 3,
                "repetitions": 12
            },
            {
                "routine": "Rutina de Iniciación y Adaptación Anatómica",
                "exercise": "Jalón al Pecho",
                "series": 3,
                "repetitions": 12
            },
            {
                "routine": "Rutina de Iniciación y Adaptación Anatómica",
                "exercise": "Aperturas en Pec Deck", # Normalizado con tu catálogo
                "series": 3,
                "repetitions": 12
            },
            {
                "routine": "Full Body de Circuitos Cardiovasculares Ligeros",
                "exercise": "Ejercicio en Máquina Elíptica", 
                "series": 3,
                "repetitions": 1
            },
            {
                "routine": "Full Body de Circuitos Cardiovasculares Ligeros",
                "exercise": "Crunch Abdominal en Máquina",
                "series": 3,
                "repetitions": 15
            },

            #// --- POTENCIA Y ATLETISMO ---
            {
                "routine": "Entrenamiento Pliométrico y de Elasticidad Muscular",
                "exercise": "Elevaciones de Piernas Colgado", # Mapeado correctamente según tu catálogo
                "series": 4,
                "repetitions": 8
            },
            {
                "routine": "Entrenamiento Pliométrico y de Elasticidad Muscular",
                "exercise": "Elevaciones de Piernas Colgado",
                "series": 3,
                "repetitions": 10
            },
            {
                "routine": "Preparación Física General de Agilidad y Esprint",
                "exercise": "Pedaleo Intenso en Air Bike",
                "series": 4,
                "repetitions": 1
            },
            {
                "routine": "Preparación Física General de Agilidad y Esprint",
                "exercise": "Paseo del Granjero con Mancuernas", # Actualizado de acuerdo a tus nombres libres
                "series": 3,
                "repetitions": 1
            }
        ]

        gym_user = [
            {
                "email": "admin.gym@fitnessapp.com",
                "username": "admin_trainer",
                "password": "AdminSecurePassword2026*",
                "is_staff": True,
                "age": None,
                "weight": None
            },
            {
                "email": "nicolas.dev@outlook.com",
                "username": "nico_fitness",
                "password": "UserPass123*",
                "is_staff": False,
                "age": 21,
                "weight": 74.5
            },
            {
                "email": "maria.gomez@gmail.com",
                "username": "maria_fit",
                "password": "MariaStrongPassword99!",
                "is_staff": False,
                "age": 28,
                "weight": 62.0
            },
            {
                "email": "carlos.mendoza@yahoo.com",
                "username": "carlitos_lift",
                "password": "CarlosBeastMode88#",
                "is_staff": False,
                "age": 35,
                "weight": 88.3
            },
            {
                "email": "laura.restrepo@outlook.com",
                "username": "laura_run",
                "password": "LauraCardioLife2026$",
                "is_staff": False,
                "age": 19,
                "weight": 55.1
            }
        ]

        user_limitations = [
            {
                "user": "nico_fitness",
                "limitation": "Síndrome del Túnel Carpiano",
                "notes": "Molestia moderada en la muñeca derecha debido a largas jornadas de programación. Evitar agarres en pronación forzada con mucho peso."
            },
            {
                "user": "maria_fit",
                "limitation": "Condromalacia Rotuliana / Dolor de Rodilla",
                "notes": "Desgaste de cartílago grado 1 en la rodilla izquierda. Dolor agudo al bajar escaleras o hacer flexiones profundas de rodilla."
            }
        ]

        userareafitnesslevel = [
            #// --- USUARIO: admin_trainer (Nivel Élite generalizado) ---
            { "user": "admin_trainer", "muscular_area": "Pecho", "fitness_level": "Avanzado" },
            { "user": "admin_trainer", "muscular_area": "Espalda", "fitness_level": "Avanzado" },
            { "user": "admin_trainer", "muscular_area": "Pecho", "fitness_level": "Avanzado" },
            { "user": "admin_trainer", "muscular_area": "Brazos", "fitness_level": "Avanzado" },
            { "user": "admin_trainer", "muscular_area": "Brazos", "fitness_level": "Avanzado" },
            { "user": "admin_trainer", "muscular_area": "Brazos", "fitness_level": "Avanzado" },
            { "user": "admin_trainer", "muscular_area": "Abdomen", "fitness_level": "Avanzado" },
            { "user": "admin_trainer", "muscular_area": "Piernas", "fitness_level": "Avanzado" },
            { "user": "admin_trainer", "muscular_area": "Piernas", "fitness_level": "Avanzado" },
            { "user": "admin_trainer", "muscular_area": "Piernas", "fitness_level": "Avanzado" },
            { "user": "admin_trainer", "muscular_area": "Piernas", "fitness_level": "Avanzado" },
            { "user": "admin_trainer", "muscular_area": "Espalda", "fitness_level": "Avanzado" },

            #// --- USUARIO: nico_fitness (Nivel Intermedio, rezagado en tren inferior por su lesión lumbar) ---
            { "user": "nico_fitness", "muscular_area": "Pecho", "fitness_level": "Intermedio" },
            { "user": "nico_fitness", "muscular_area": "Espalda", "fitness_level": "Intermedio" },
            { "user": "nico_fitness", "muscular_area": "Pecho", "fitness_level": "Intermedio" },
            { "user": "nico_fitness", "muscular_area": "Brazos", "fitness_level": "Intermedio" },
            { "user": "nico_fitness", "muscular_area": "Brazos", "fitness_level": "Intermedio" },
            { "user": "nico_fitness", "muscular_area": "Brazos", "fitness_level": "Intermedio" },
            { "user": "nico_fitness", "muscular_area": "Abdomen", "fitness_level": "Intermedio" },
            { "user": "nico_fitness", "muscular_area": "Piernas", "fitness_level": "Principiante" },
            { "user": "nico_fitness", "muscular_area": "Piernas", "fitness_level": "Principiante" },
            { "user": "nico_fitness", "muscular_area": "Piernas", "fitness_level": "Principiante" },
            { "user": "nico_fitness", "muscular_area": "Piernas", "fitness_level": "Principiante" },
            { "user": "nico_fitness", "muscular_area": "Espalda", "fitness_level": "Intermedio" },

            #// --- USUARIO: maria_fit (Nivel Principiante/Intermedio, fuerte en tren superior y core, adaptándose en rodillas) ---
            { "user": "maria_fit", "muscular_area": "Pecho", "fitness_level": "Principiante" },
            { "user": "maria_fit", "muscular_area": "Espalda", "fitness_level": "Intermedio" },
            { "user": "maria_fit", "muscular_area": "Pecho", "fitness_level": "Principiante" },
            { "user": "maria_fit", "muscular_area": "Brazos", "fitness_level": "Principiante" },
            { "user": "maria_fit", "muscular_area": "Brazos", "fitness_level": "Principiante" },
            { "user": "maria_fit", "muscular_area": "Brazos", "fitness_level": "Principiante" },
            { "user": "maria_fit", "muscular_area": "Abdomen", "fitness_level": "Intermedio" },
            { "user": "maria_fit", "muscular_area": "Piernas", "fitness_level": "Principiante" },
            { "user": "maria_fit", "muscular_area": "Piernas", "fitness_level": "Principiante" },
            { "user": "maria_fit", "muscular_area": "Piernas", "fitness_level": "Intermedio" },
            { "user": "maria_fit", "muscular_area": "Piernas", "fitness_level": "Principiante" },
            { "user": "maria_fit", "muscular_area": "Espalda", "fitness_level": "Principiante" },

            #// --- USUARIO: carlitos_lift (Nivel Avanzado en empujes y tracciones, limitado en hombro) ---
            { "user": "carlitos_lift", "muscular_area": "Pecho", "fitness_level": "Avanzado" },
            { "user": "carlitos_lift", "muscular_area": "Espalda", "fitness_level": "Avanzado" },
            { "user": "carlitos_lift", "muscular_area": "Pecho", "fitness_level": "Principiante" },
            { "user": "carlitos_lift", "muscular_area": "Brazos", "fitness_level": "Avanzado" },
            { "user": "carlitos_lift", "muscular_area": "Brazos", "fitness_level": "Avanzado" },
            { "user": "carlitos_lift", "muscular_area": "Brazos", "fitness_level": "Intermedio" },
            { "user": "carlitos_lift", "muscular_area": "Abdomen", "fitness_level": "Intermedio" },
            { "user": "carlitos_lift", "muscular_area": "Piernas", "fitness_level": "Avanzado" },
            { "user": "carlitos_lift", "muscular_area": "Piernas", "fitness_level": "Avanzado" },
            { "user": "carlitos_lift", "muscular_area": "Piernas", "fitness_level": "Intermedio" },
            { "user": "carlitos_lift", "muscular_area": "Piernas", "fitness_level": "Avanzado" },
            { "user": "carlitos_lift", "muscular_area": "Espalda", "fitness_level": "Intermedio" },

            #// --- USUARIO: laura_run (Nivel Principiante en fuerza general, gran enfoque en piernas/cardio) ---
            { "user": "laura_run", "muscular_area": "Pecho", "fitness_level": "Principiante" },
            { "user": "laura_run", "muscular_area": "Espalda", "fitness_level": "Principiante" },
            { "user": "laura_run", "muscular_area": "Pecho", "fitness_level": "Principiante" },
            { "user": "laura_run", "muscular_area": "Brazos", "fitness_level": "Principiante" },
            { "user": "laura_run", "muscular_area": "Brazos", "fitness_level": "Principiante" },
            { "user": "laura_run", "muscular_area": "Brazos", "fitness_level": "Principiante" },
            { "user": "laura_run", "muscular_area": "Abdomen", "fitness_level": "Intermedio" },
            { "user": "laura_run", "muscular_area": "Piernas", "fitness_level": "Intermedio" },
            { "user": "laura_run", "muscular_area": "Piernas", "fitness_level": "Intermedio" },
            { "user": "laura_run", "muscular_area": "Piernas", "fitness_level": "Intermedio" },
            { "user": "laura_run", "muscular_area": "Piernas", "fitness_level": "Intermedio" },
            { "user": "laura_run", "muscular_area": "Espalda", "fitness_level": "Principiante" }
        ]

        trainingplan = [
            {
                "user": "nico_fitness",
                "goal": "Hipertrofia Muscular",
                "weekly_frequency": 4,
                "duration_weeks": 8,
                "status": "Active"
            },
            {
                "user": "laura_run",
                "goal": "Resistencia Cardiovascular",
                "weekly_frequency": 5,
                "duration_weeks": 12,
                "status": "Active"
            }
        ]

        for data in goals_data:
            payload = self._sanitize_payload(data)
            goal, created = self._get_or_create_named(
                models.Goal,
                payload["name"],
                defaults={"description": payload["description"]},
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"✔ Goal creado: {goal.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"⚠ Goal ya existente: {goal.name}"))

        for data in limitations:
            payload = self._sanitize_payload(data)
            limitation, created = self._get_or_create_named(
                models.Limitation,
                payload["name"],
                defaults={"description": payload["description"]},
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"✔ Limitación creada: {limitation.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"⚠ Limitación ya existente: {limitation.name}"))

        for data in areas:
            payload = self._sanitize_payload(data)
            area, created = self._get_or_create_named(models.MuscularArea, payload["name"])
            if created:
                self.stdout.write(self.style.SUCCESS(f"✔ Área muscular creada: {area.name}"))

        for data in machines:
            payload = self._sanitize_payload(data)
            machine, created = self._get_or_create_named(models.Machine, payload["name"])
            if created:
                self.stdout.write(self.style.SUCCESS(f"✔ Máquina creada: {machine.name}"))

        for data in routines:
            payload = self._sanitize_payload(data)
            routine, created = self._get_or_create_named(models.Routine, payload["name"])
            if created:
                self.stdout.write(self.style.SUCCESS(f"✔ Rutina creada: {routine.name}"))

        for data in fitness_levels:
            payload = self._sanitize_payload(data)
            fitness_level, created = self._get_or_create_named(
                models.FitnessLevel,
                payload["name"],
                defaults={
                    "series_multiplier": payload["series_multiplier"],
                    "repetitions_multiplier": payload["repetitions_multiplier"],
                },
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"✔ Nivel de fitness creado: {fitness_level.name}"))

        for data in exercises_data:
            payload = self._sanitize_payload(data)
            muscular_area = self._get_or_create_named(models.MuscularArea, payload["muscle_area"])[0]
            machine = self._get_or_create_named(models.Machine, payload["machine"])[0] if payload.get("machine") else None
            exercise, created = models.Exercise.objects.get_or_create(
                name=payload["name"],
                defaults={
                    "description": payload["description"],
                    "muscular_area_id": muscular_area.id,
                    "machine_id": machine.id if machine else None,
                },
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"✔ Ejercicio creado: {exercise.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"⚠ Ejercicio ya existente: {exercise.name}"))

        for data in exercise_limitation:
            payload = self._sanitize_payload(data)
            limitation = self._get_named(models.Limitation, payload["limitation"])
            exercise = self._get_named(models.Exercise, payload["exercise"])
            if limitation is None or exercise is None:
                self.stdout.write(self.style.ERROR(f"❌ No se pudo relacionar {payload['exercise']} con {payload['limitation']}"))
                continue
            relation, created = models.ExerciseLimitation.objects.get_or_create(
                exercise_id=exercise.id,
                limitation_id=limitation.id,
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"✔ Relación ejercicio-limitación creada: {exercise.name}"))

        for data in goal_routine:
            payload = self._sanitize_payload(data)
            goal = self._get_named(models.Goal, payload["goal"])
            routine = self._get_named(models.Routine, payload["routine"])
            if goal is None or routine is None:
                self.stdout.write(self.style.ERROR(f"❌ No se pudo relacionar {payload['routine']} con {payload['goal']}"))
                continue
            relation, created = models.GoalRoutine.objects.get_or_create(goal_id=goal.id, routine_id=routine.id)
            if created:
                self.stdout.write(self.style.SUCCESS(f"✔ Relación meta-rutina creada: {routine.name}"))

        for data in routine_exercise:
            payload = self._sanitize_payload(data)
            routine = self._get_named(models.Routine, payload["routine"])
            exercise = self._get_named(models.Exercise, payload["exercise"])
            if routine is None or exercise is None:
                self.stdout.write(self.style.ERROR(f"❌ No se pudo relacionar {payload['exercise']} con {payload['routine']}"))
                continue
            relation, created = models.RoutineExercise.objects.get_or_create(
                routine_id=routine.id,
                exercise_id=exercise.id,
                defaults={
                    "series": payload["series"],
                    "repetitions": payload["repetitions"],
                },
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"✔ Ejercicio de rutina creado: {routine.name}"))

        for data in gym_user:
            result = register_user(
                email=data["email"],
                username=data["username"],
                password=data["password"],
            )

            if result["success"]:
                user = get_user_by_correo(data["email"])
                if user is None:
                    self.stdout.write(self.style.ERROR(f"❌ No se pudo recuperar al usuario: {data['username']}"))
                    continue

                user.is_staff = data["is_staff"]
                if not data["is_staff"]:
                    user.age = data["age"]
                    user.weight = data["weight"]
                user.save()
                self.stdout.write(self.style.SUCCESS(f"✔ Usuario creado y configurado: {user.username}"))
            else:
                self.stdout.write(self.style.ERROR(f"❌ Error al registrar {data['username']}: {result['message']}"))

        for data in user_limitations:
            payload = self._sanitize_payload(data)
            user = models.GymUser.objects.filter(username=payload["user"]).first()
            limitation = self._get_named(models.Limitation, payload["limitation"])
            if user is None or limitation is None:
                self.stdout.write(self.style.ERROR(f"❌ No se pudo crear la limitación para {payload['user']}"))
                continue
            relation, created = models.UserLimitation.objects.get_or_create(
                user_id=user.id,
                limitation_id=limitation.id,
                defaults={"notes": payload.get("notes", "")},
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"✔ Limitación de usuario creada: {user.username}"))

        for data in userareafitnesslevel:
            payload = self._sanitize_payload(data)
            user = models.GymUser.objects.filter(username=payload["user"]).first()
            muscular_area = self._get_named(models.MuscularArea, payload["muscular_area"])
            fitness_level = self._get_named(models.FitnessLevel, payload["fitness_level"])
            if user is None or muscular_area is None or fitness_level is None:
                self.stdout.write(self.style.ERROR(f"❌ No se pudo asignar el nivel de fitness para {payload['user']}"))
                continue
            relation, created = models.UserAreaFitnessLevel.objects.get_or_create(
                user_id=user.id,
                muscular_area_id=muscular_area.id,
                defaults={"fitness_level_id": fitness_level.id},
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"✔ Nivel de fitness por área creado: {user.username}"))

        for data in trainingplan:
            payload = self._sanitize_payload(data)
            user = models.GymUser.objects.filter(username=payload["user"]).first()
            goal = self._get_named(models.Goal, payload["goal"])
            if user is None or goal is None:
                self.stdout.write(self.style.ERROR(f"❌ No se pudo crear el plan para {payload['user']}"))
                continue
            plan, created = models.TrainingPlan.objects.get_or_create(
                user_id=user.id,
                goal_id=goal.id,
                defaults={
                    "weekly_frequency": payload["weekly_frequency"],
                    "duration_weeks": payload["duration_weeks"],
                    "status": str(payload.get("status", "active")).lower(),
                    "start_date": payload.get("start_date", date.today()),
                },
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"✔ Plan creado: {plan.user.username}"))

        active_plans = models.TrainingPlan.objects.filter(status__iexact="active")
        for plan in active_plans:
            total_sessions = plan.weekly_frequency * plan.duration_weeks
            routines = list(models.Routine.objects.filter(goalroutine__goal=plan.goal))

            if not routines:
                self.stdout.write(self.style.ERROR(f"❌ No hay rutinas sembradas para la meta: {plan.goal.name}"))
                continue

            self.stdout.write(f"Generando {total_sessions} sesiones para el plan de {plan.user.username}...")
            for current_session in range(1, total_sessions + 1):
                routine_to_assign = routines[(current_session - 1) % len(routines)]
                models.PlanRoutine.objects.get_or_create(
                    plan_id=plan.id,
                    session_number=current_session,
                    defaults={"routine_id": routine_to_assign.id},
                )

            self.stdout.write(self.style.SUCCESS(f"✔ ¡PlanRoutine poblado con éxito para {plan.user.username}!"))

        workoutlog = [
            {
                "plan_user": "nico_fitness",
                "session_number": 1,
                "logged_at": "2026-07-01T08:30:00Z",
            },
            {
                "plan_user": "nico_fitness",
                "session_number": 2,
                "logged_at": "2026-07-02T09:15:00Z",
            },
            {
                "plan_user": "nico_fitness",
                "session_number": 3,
                "logged_at": "2026-07-04T08:00:00Z",
            },
            {
                "plan_user": "nico_fitness",
                "session_number": 4,
                "logged_at": "2026-07-05T10:00:00Z",
            },
            {
                "plan_user": "laura_run",
                "session_number": 1,
                "logged_at": "2026-07-01T06:00:00Z",
            },
            {
                "plan_user": "laura_run",
                "session_number": 2,
                "logged_at": "2026-07-02T06:30:00Z",
            },
            {
                "plan_user": "laura_run",
                "session_number": 3,
                "logged_at": "2026-07-03T07:00:00Z",
            },
        ]

        for data in workoutlog:
            user = models.GymUser.objects.filter(username=data["plan_user"]).first()
            if user is None:
                self.stdout.write(self.style.ERROR(f"❌ Usuario no encontrado: {data['plan_user']}"))
                continue

            plan = models.TrainingPlan.objects.filter(user=user, status="active").first()
            if plan is None:
                self.stdout.write(self.style.ERROR(f"❌ No se encontró un plan activo para: {data['plan_user']}"))
                continue

            plan_routine = models.PlanRoutine.objects.filter(plan=plan, session_number=data["session_number"]).first()
            if plan_routine is None:
                self.stdout.write(self.style.ERROR(f"❌ No existe la sesión {data['session_number']} en el plan de {data['plan_user']}"))
                continue

            workout_log, created = models.WorkoutLog.objects.get_or_create(
                plan_routine_id=plan_routine.id,
                defaults={"logged_at": data["logged_at"]},
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"✔ Log registrado: {user.username} completó la sesión n.º {data['session_number']} el {data['logged_at']}"))

        self.stdout.write(self.style.SUCCESS("¡Base de datos sembrada con éxito!"))