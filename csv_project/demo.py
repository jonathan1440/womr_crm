import csv_interface

# Define the path to the sample .csv file
sample_csv_path = "csv_project/sample.csv"

# Read data from the sample .csv file
data = csv_interface.read_csv(sample_csv_path)
print("Data read from sample.csv:")
print(data)

# Modify the data
data.append({"name": "David", "age": 28, "city": "San Francisco"})

# Write the modified data back to the .csv file
csv_interface.write_csv(sample_csv_path, data, fieldnames=["name", "age", "city"])

# Read the data again to verify the changes
data = csv_interface.read_csv(sample_csv_path)
print("Data after modification:")
print(data)