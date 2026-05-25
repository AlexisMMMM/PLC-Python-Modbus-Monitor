import pymodbus
from pymodbus.client import ModbusTcpClient
import time
import csv
from datetime import datetime

# Conexión al servidor Modbus TCP de CODESYS
client = ModbusTcpClient(host='127.0.0.1', port=502)

# Archivo CSV para loggear datos
csv_file = 'plc_data_log.csv'

def main():
    if not client.connect():
        print("Error: No se pudo conectar al PLC")
        return

    print("Conectado al PLC — iniciando monitoreo...")
    print("-" * 40)

    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Sensor_Object', 'Motor_Running'])

        try:
            while True:
                # Leer Sensor_Object (Coil 0)
                sensor = client.read_coils(address=0, count=1)
                # Leer Motor_Running (Discrete Input 0)
                motor = client.read_discrete_inputs(address=0, count=1)

                sensor_val = sensor.bits[0] if not sensor.isError() else None
                motor_val = motor.bits[0] if not motor.isError() else None

                timestamp = datetime.now().strftime('%H:%M:%S')

                print(f"[{timestamp}] Sensor_Object: {sensor_val} | Motor_Running: {motor_val}")

                writer.writerow([timestamp, sensor_val, motor_val])
                file.flush()

                time.sleep(1)

        except KeyboardInterrupt:
            print("\nMonitoreo detenido.")
            client.close()

if __name__ == "__main__":
    main()