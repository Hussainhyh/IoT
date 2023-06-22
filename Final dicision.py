import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# Load the labeled data from a CSV file
data = pd.read_csv('H:\\thesis\\Output\\data\\accel_data.csv')

# Split the data into features and labels
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

# Load the new data from a CSV file
new_data = pd.read_csv('H:\\thesis\\last stand\\accel_data.csv')

# Calculate the magnitude of the acceleration vector
X_new = new_data[['accel_x', 'accel_y', 'accel_z']]
X_new['accel_mag'] = (X_new['accel_x']**2 + X_new['accel_y']**2 + X_new['accel_z']**2)**0.5

# Use the trained classifier to predict on the new data
y_pred = clf.predict(X_new)

# Print the predicted labels for the new data
print('Predicted labels for the new data:')
print(y_pred)
