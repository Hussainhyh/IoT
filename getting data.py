import serial
import json

ser = serial.Serial('COM3', 115200)  # replace with the appropriate port and baud rate

while True:
    line = ser.readline().decode('utf-8').strip()
    if line.startswith('Telemetry message sent:'):
        
        try:
            start_index = line.find('{') # find the start index of the JSON data
            end_index = line.rfind('}') + 1 # find the end index of the JSON data
            json_data = line[start_index:end_index] # extract the JSON data as a string
            data = json.loads(json_data) # parse the JSON data
            
            if 'accelerometerX' in data:
                accel_x = data['accelerometerX']
                accel_y = data['accelerometerY']
                accel_z = data['accelerometerZ']
                
                print(f"Accel: x={accel_x}, y={accel_y}, z={accel_z}")
            else:
                """print("No accelerometer data found")"""
            
            
        except json.JSONDecodeError:
            print(f"Error: could not parse data from line: {line}")
    else:
        print(f"Ignoring line: {line}")
