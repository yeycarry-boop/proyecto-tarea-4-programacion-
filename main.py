import logging  # Línea 1: Importación estándar sin caracteres ocultos
from abc import ABC, abstractmethod

# Configuración del Sistema de Logs de Software FJ
logging.basicConfig(
    filename='software_fj.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# --- EXCEPCIONES PERSONALIZADAS ---
class SoftwareFJError(Exception):
    """Clase base para errores del sistema Yeiron Mora."""
    pass

class ValidacionDatoError(SoftwareFJError):
    """Error para datos inválidos o parámetros faltantes."""
    pass

# --- CLASES BASE (ABSTRACCIÓN) ---
class Entidad(ABC):
    def __init__(self, id_entidad):
        self._id = id_entidad

    @property
    def id(self):
        return self._id

    @abstractmethod
    def __str__(self):
        pass

# --- CLASE CLIENTE (ENCAPSULACIÓN) ---
class Cliente(Entidad):
    def __init__(self, id_cliente, nombre, correo):
        super().__init__(id_cliente)
        # Validación estricta de datos
        if not nombre or "@" not in str(correo):
            raise ValidacionDatoError(f"Datos de cliente inválidos: {nombre}")
        self.__nombre = nombre  # Atributo privado
        self.__correo = correo

    def __str__(self):
        return f"Cliente: {self.__nombre} (ID: {self.id})"

# --- CLASES DE SERVICIO (HERENCIA Y POLIMORFISMO) ---
class Servicio(Entidad, ABC):
    def __init__(self, id_servicio, nombre, costo_base):
        super().__init__(id_servicio)
        self.nombre = nombre
        self.costo_base = costo_base

    @abstractmethod
    def calcular_total(self, cantidad, **kwargs):
        pass

class ReservaSala(Servicio):
    def calcular_total(self, horas, limpieza=False):
        return (self.costo_base * horas) + (35 if limpieza else 0)

class AlquilerEquipo(Servicio):
    def calcular_total(self, dias, seguro=True):
        tasa = 1.12 if seguro else 1.0
        return (self.costo_base * dias) * tasa

# --- CLASE RESERVA (MANEJO DE EXCEPCIONES) ---
class Reserva:
    def __init__(self, id_reserva, cliente, servicio, duracion, **kwargs):
        self.id_reserva = id_reserva
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.extras = kwargs

    def procesar(self):
        try:
            # Validaciones de seguridad
            if not isinstance(self.cliente, Cliente):
                raise ValidacionDatoError("El cliente no es un objeto válido.")
            if self.duracion <= 0:
                raise ValueError("La duración debe ser positiva.")

            # Polimorfismo en acción
            monto = self.servicio.calcular_total(self.duracion, **self.extras)
            logging.info(f"Venta {self.id_reserva} exitosa por ${monto}")
            return monto

        except Exception as e:
            logging.error(f"Error en {self.id_reserva}: {e}")
            raise  # Permite que el main gestione la continuidad