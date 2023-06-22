import serial
import json
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

ser = serial.Serial('COM3', 115200) 

# Load the labeled data from a CSV file
data = pd.read_csv('H:\\thesis\\Output\\data\\accel_data.csv')

X = data[['accel_x', 'accel_y', 'accel_z']]
y = data['label']

# Split the data into training, validation, and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.25, random_state=42)

# Calculate the magnitude of the acceleration vector
X_train['accel_mag'] = (X_train['accel_x']**2 + X_train['accel_y']**2 + X_train['accel_z']**2)**0.5
X_val['accel_mag'] = (X_val['accel_x']**2 + X_val['accel_y']**2 + X_val['accel_z']**2)**0.5
X_test['accel_mag'] = (X_test['accel_x']**2 + X_test['accel_y']**2 + X_test['accel_z']**2)**0.5

# Train a decision tree classifier on the training data
clf = DecisionTreeClassifier(max_depth=5, min_samples_split=5, random_state=42)
clf.fit(X_train, y_train)

# Evaluate the accuracy of the decision tree classifier on the validation data
y_val_pred = clf.predict(X_val)
val_accuracy = accuracy_score(y_val, y_val_pred)
print('Accuracy on the validation data: {:.2f}'.format(val_accuracy))

# Evaluate the accuracy of the decision tree classifier on the test data
y_test_pred = clf.predict(X_test)
test_accuracy = accuracy_score(y_test, y_test_pred)
print('Accuracy on the test data: {:.2f}'.format(test_accuracy))
accel_data = []  # initialize empty list to store accelerometer data
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
                
                accel_data.append([accel_x, accel_y, accel_z])  # add accelerometer data to list
                # Convert the list of new data to a DataFrame
                new_data_df = pd.DataFrame(accel_data, columns=['accel_x', 'accel_y', 'accel_z'])

                # Calculate the magnitude of the acceleration vector
                new_data_df['accel_mag'] = (new_data_df['accel_x']**2 + new_data_df['accel_y']**2 + new_data_df['accel_z']**2)**0.5

                # Use the trained classifier to predict on the new data
                y_pred = clf.predict(new_data_df)

                # Print the predicted labels for the new data
                print('Prediction of the hand movement')
                print(y_pred)
                accel_data.clear()
                
            else:
                """print("No accelerometer data found")"""
            
            
        except json.JSONDecodeError:
            print(f"Error: could not parse data from line: {line}")
    else:
        print(f"Ignoring line: {line}")
ser.close()  # close the serial port when done
