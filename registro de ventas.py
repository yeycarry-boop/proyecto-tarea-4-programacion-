import logging

class RegistroVentas:
    def __init__(self):
        self._ventas = []

    def registrar(self, reserva):
        try:
            if reserva.estado != "CONFIRMADA":
                raise ValueError("No se puede registrar venta")

            self._ventas.append(reserva)
            logging.info(f"Venta registrada: {reserva.id}")

        except Exception as e:
            logging.error(f"Error venta: {e}")

    def obtener_ventas(self):
        return self._ventas