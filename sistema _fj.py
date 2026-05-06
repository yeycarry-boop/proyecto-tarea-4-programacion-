import logging
from abc import ABC, abstractmethod

# =========================
# EXCEPCIONES
# =========================
class SistemaFJError(Exception):
    pass

class ValidacionError(SistemaFJError):
    pass

class OperacionError(SistemaFJError):
    pass


# =========================
# CLASE ABSTRACTA
# =========================
class Entidad(ABC):
    def __init__(self, id):
        if not id:
            raise ValidacionError("ID inválido")
        self._id = id

    @property
    def id(self):
        return self._id

    @abstractmethod
    def mostrar(self):
        pass


# =========================
# CLIENTE (ENCAPSULADO)
# =========================
class Cliente(Entidad):
    def __init__(self, id, nombre, email):
        super().__init__(id)

        if len(nombre) < 3:
            raise ValidacionError("Nombre inválido")
        if "@" not in email:
            raise ValidacionError("Email inválido")

        self.__nombre = nombre
        self.__email = email

    def get_nombre(self):
        return self.__nombre

    def mostrar(self):
        return f"{self.__nombre} ({self.id})"


# =========================
# SERVICIO ABSTRACTO
# =========================
class Servicio(Entidad, ABC):
    def __init__(self, id, nombre, tarifa):
        super().__init__(id)

        if tarifa <= 0:
            raise ValidacionError("Tarifa inválida")

        self._nombre = nombre
        self._tarifa = tarifa

    @abstractmethod
    def calcular_costo(self, tiempo, **kwargs):
        pass

    def validar(self, tiempo):
        if tiempo <= 0:
            raise OperacionError("Tiempo inválido")


# =========================
# SERVICIOS (POLIMORFISMO)
# =========================
class Sala(Servicio):
    def calcular_costo(self, horas, **kwargs):
        self.validar(horas)
        costo = self._tarifa * horas
        if kwargs.get("proyector", False):
            costo += 30
        return costo


class Equipo(Servicio):
    def calcular_costo(self, dias, **kwargs):
        self.validar(dias)
        seguro = kwargs.get("seguro", True)
        return (self._tarifa * dias) * (1.1 if seguro else 1)


class Asesoria(Servicio):
    def calcular_costo(self, sesiones, **kwargs):
        self.validar(sesiones)
        nivel = kwargs.get("nivel", "Junior")
        niveles = {"Junior": 1, "Senior": 1.5, "Master": 2}

        if nivel not in niveles:
            raise ValidacionError("Nivel inválido")

        return (self._tarifa * sesiones) * niveles[nivel]


# =========================
# RESERVA
# =========================
class Reserva:
    def __init__(self, id, cliente, servicio, tiempo, **kwargs):
        if not isinstance(cliente, Cliente):
            raise ValidacionError("Cliente inválido")

        if not isinstance(servicio, Servicio):
            raise ValidacionError("Servicio inválido")

        self.id = id
        self.cliente = cliente
        self.servicio = servicio
        self.tiempo = tiempo
        self.detalles = kwargs
        self.estado = "CREADA"

    def confirmar(self):
        self.estado = "CONFIRMADA"

    def cancelar(self):
        self.estado = "CANCELADA"

    def procesar(self):
        try:
            total = self.servicio.calcular_costo(self.tiempo, **self.detalles)

        except (ValidacionError, OperacionError) as e:
            self.estado = "ERROR_CONTROLADO"
            logging.error(f"{self.id} - {e}")
            raise SistemaFJError("Error en reserva") from e

        except Exception as e:
            self.estado = "ERROR_CRITICO"
            logging.critical(f"{self.id} - {e}")
            raise

        else:
            self.confirmar()
            print(f"✔ Reserva {self.id}: ${total:.2f}")

        finally:
            logging.info(f"{self.id} estado final: {self.estado}")


# =========================
# SISTEMA
# =========================
class SistemaFJ:
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def agregar_cliente(self, cliente):
        self.clientes.append(cliente)

    def agregar_servicio(self, servicio):
        self.servicios.append(servicio)

    def crear_reserva(self, *args, **kwargs):
        try:
            r = Reserva(*args, **kwargs)
            self.reservas.append(r)
            return r
        except Exception as e:
            logging.error(f"Error creando reserva: {e}")
            return None