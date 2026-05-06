import logging
from registro_ventas import (
    Cliente, 
    ReservaSala, 
    AlquilerEquipo, 
    Reserva, 
    SoftwareFJError
)

def imprimir_encabezado():
    """Muestra la identidad del desarrollador y del sistema."""
    print("=" * 60)
    print("SISTEMA DE GESTIÓN INTEGRAL - SOFTWARE FJ")
    print("Desarrollado por: YEIRON MORA") # Firma solicitada
    print("=" * 60)
    print("\nIniciando simulación de 10 operaciones...\n")

def ejecutar_sistema():
    imprimir_encabezado()

    # 1. Configuración de datos maestros (Listas internas)
    try:
        cliente_a = Cliente("C-01", "Yeiron Mora", "yeiron@softwarefj.com")
        cliente_b = Cliente("C-02", "Corporación Global", "info@global.com")
        
        servicios = [
            ReservaSala("S-01", "Sala de Juntas VIP", 80.0),
            AlquilerEquipo("E-01", "Estación de Trabajo G9", 45.0)
        ]
    except Exception as e:
        logging.critical(f"Error al inicializar datos: {e}")
        print(f"Fallo crítico inicial: {e}")
        return

    # 2. Definición de Operaciones (Mezcla de éxitos y fallos controlados)
    # Formato: (ID, Cliente, Servicio, Cantidad, Argumentos Extras)
    operaciones = [
        ("V-101", cliente_a, servicios[0], 5, {"limpieza": True}),    # OK
        ("V-102", cliente_b, servicios[1], 2, {"seguro": True}),     # OK
        ("V-103", cliente_a, servicios[1], -1, {}),                  # ERROR: Cantidad negativa
        ("V-104", "Dato Corrupto", servicios[0], 10, {}),            # ERROR: Tipo de dato
        ("V-105", cliente_b, servicios[0], 4, {"limpieza": False}),  # OK
        ("V-106", cliente_a, servicios[1], 0, {}),                   # ERROR: Cantidad cero
        ("V-107", None, servicios[1], 3, {}),                        # ERROR: Cliente nulo
        ("V-108", cliente_b, servicios[1], 7, {"seguro": False}),    # OK
        ("V-109", cliente_a, servicios[0], 2, {"limpieza": True}),   # OK
        ("V-110", cliente_b, servicios[1], 1, {"seguro": True}),     # OK
    ]

    # 3. Procesamiento Robusto
    ventas_exitosas = 0
    monto_total = 0.0

    for id_v, cli, serv, cant, extras in operaciones:
        try:
            # Creación del objeto Reserva
            reserva = Reserva(id_v, cli, serv, cant, **extras)
            # Ejecución del procesamiento con polimorfismo
            monto = reserva.procesar()
            
            monto_total += monto
            ventas_exitosas += 1
            
        except Exception as e:
            # Captura cualquier error, lo registra en log y permite continuar
            logging.warning(f"Operación {id_v} saltada. Motivo: {e}")
            print(f"--> [AVISO] La operación {id_v} falló pero el sistema continúa.")
        
        finally:
            print("-" * 50)

    # 4. Cierre y Resultados
    print("\n" + "=" * 60)
    print("FINALIZACIÓN DEL PROCESO")
    print(f"Operaciones totales procesadas con éxito: {ventas_exitosas}/10")
    print(f"Recaudación total: ${monto_total:,.2f}")
    print(f"Firma del responsable: YEIRON MORA") # Firma de salida
    print("=" * 60)
    print("Detalles técnicos almacenados en: software_fj.log")

if __name__ == "__main__":
    ejecutar_sistema()