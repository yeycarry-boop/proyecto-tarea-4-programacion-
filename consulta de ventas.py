class ConsultaVentas:

    @staticmethod
    def total_ventas(ventas):
        total = 0
        for v in ventas:
            try:
                total += v.servicio.calcular_costo(v.tiempo, **v.detalles)
            except Exception:
                continue
        return total

    @staticmethod
    def mostrar_resumen(ventas):
        print("\n--- RESUMEN ---")
        for v in ventas:
            print(f"{v.id} | {v.cliente.get_nombre()} | {v.estado}")