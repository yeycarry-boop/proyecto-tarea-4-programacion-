import logging
from abc import ABC, abstractmethod

# Configuración del archivo de LOGS para registrar eventos y errores
logging.basicConfig(
    filename='software_fj.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# --- EXCEPCIONES PERSONALIZADAS ---
class SoftwareFJError(Exception):
    """Clase base para excepciones del sistema."""
    pass

class ValidacionDatoError(SoftwareFJError):
    """Se lanza cuando los datos de entrada son incorrectos."""
    pass

# --- CLASES BASE Y ABSTRACCIÓN ---
class Entidad(ABC):
    def __init__(self, id_entidad):
        self._id = id_entidad # Atributo protegido

    @property
    def id(self):
        return self._id

    @abstractmethod
    def __str__(self):
        pass

# --- CLASE CLIENTE ---
class Cliente(Entidad):
    def __init__(self, id_cliente, nombre, correo):
        super().__init__(id_cliente)
        # Validación estricta
        if not nombre or "@" not in correo:
            raise ValidacionDatoError(f"Datos de cliente inválidos: {nombre}")
        self.__nombre = nombre # Atributo privado
        self.__correo = correo

    def __str__(self):
        return f"Cliente: {self.__nombre} (ID: {self.id})"

# --- JERARQUÍA DE SERVICIOS (POLIMORFISMO) ---
class Servicio(Entidad, ABC):
    def __init__(self, id_servicio, nombre, costo_base):
        super().__init__(id_servicio)
        self.nombre = nombre
        self.costo_base = costo_base

    @abstractmethod
    def calcular_cobro(self, cantidad, **kwargs):
        pass

class ReservaSala(Servicio):
    def calcular_cobro(self, horas, limpieza=False):
        total = self.costo_base * horas
        if limpieza: total += 30
        return total

class AlquilerEquipo(Servicio):
    def calcular_cobro(self, dias, seguro=True):
        tasa = 1.10 if seguro else 1.0
        return (self.costo_base * dias) * tasa

# --- CLASE RESERVA (GESTIÓN E INTEGRACIÓN) ---
class Reserva:
    def __init__(self, id_reserva, cliente, servicio, cantidad, **kwargs):
        self.id_reserva = id_reserva
        self.cliente = cliente
        self.servicio = servicio
        self.cantidad = cantidad
        self.opciones = kwargs

    def procesar(self):
        try:
            # Verificación de integridad
            if not isinstance(self.cliente, Cliente):
                raise ValidacionDatoError("El objeto cliente no es válido.")
            if self.cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor a cero.")

            # Polimorfismo
            total = self.servicio.calcular_cobro(self.cantidad, **self.opciones)
            
            logging.info(f"Reserva {self.id_reserva} exitosa. Total: ${total}")
            print(f"ÉXITO: {self.servicio.nombre} reservado para {self.cliente}")
            return total

        except Exception as e:
            # Registro de cualquier error en el log
            logging.error(f"Error en Reserva {self.id_reserva}: {e}")
            print(f"ERROR en {self.id_reserva}: {e}")
            raise # Re-lanzar para que el main lo maneje