import logging

def obtener_resumen_ventas():
    try:
        print("\n--- CONSULTA DE VENTAS REGISTRADAS ---")
        with open("ventas.txt", "r") as f:
            lineas = f.readlines()
            if not lineas:
                print("No hay ventas registradas.")
                return

            total_acumulado = 0
            for linea in lineas:
                id_v, cli, serv, total = linea.strip().split(",")
                print(f"Reserva: {id_v} | Cliente ID: {cli} | Servicio: {serv} | Total: ${total}")
                total_acumulado += float(total)
            
            print(f"\nINGRESOS TOTALES: ${total_acumulado:.2f}")
            
    except FileNotFoundError:
        print("El archivo de ventas aún no existe.")
    except Exception as e:
        logging.error(f"Error al consultar ventas: {e}")
        print("Ocurrió un error al procesar la consulta.")