import time
import serial
import json
import csv
import os

ser = serial.Serial('COM3', 115200)  # replace with the appropriate port and baud rate

output_dir = 'H:\\thesis\\last stand'
output_file = os.path.join(output_dir, 'accel_data.csv')

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(output_file, 'w', newline='') as csvfile:
    fieldnames = ['label', 'accel_x', 'accel_y', 'accel_z']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    start_time = time.time()  # record the start time
    while time.time() - start_time <= 120:  # run for 1 minute
        line = ser.readline().decode('utf-8').strip()
        if line.startswith('Telemetry message sent:'):
            try:
                start_index = line.find('{')
                end_index = line.rfind('}') + 1
                json_data = line[start_index:end_index]
                data = json.loads(json_data)

                if 'accelerometerX' in data:
                    accel_x = data['accelerometerX']
                    accel_y = data['accelerometerY']
                    accel_z = data['accelerometerZ']
                    print(f"Accel: x={accel_x}, y={accel_y}, z={accel_z}")
                    writer.writerow({'label': 'accel_data', 'accel_x': accel_x, 'accel_y': accel_y, 'accel_z': accel_z})

                else:
                    """print("No accelerometer data found")"""

            except json.JSONDecodeError:
                print(f"Error: could not parse data from line: {line}")
        else:
            print(f"Ignoring line: {line}")

ser.close()  # close the serial port when done















