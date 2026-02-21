import pandas as pd

# Take list input (comma-separated values)
user_input = input("Enter list elements separated by commas: ")

# Convert to Python list
data_list = [item.strip() for item in user_input.split(",")]

# Convert to DataFrame/Series
series_data = pd.Series(data_list)

# Shuffle using pd.sample with random_state
shuffled = series_data.sample(frac=1, random_state=42).tolist()

print("Shuffled List:", shuffled)
