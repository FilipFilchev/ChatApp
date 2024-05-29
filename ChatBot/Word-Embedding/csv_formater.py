import pandas as pd

# Load the data
data_path = './ChatBot_QA.xlsx'
data = pd.read_excel(data_path, header=None)

# Remove header row if present (assuming the first row might be a header)
if data.iloc[0, 0].strip().lower() == 'въпрос':
    data = data.iloc[1:]

# Set column names
data.columns = ['Question', 'Answer']

# Save as CSV
data.to_csv('./dataset.csv', index=False)

# Display the first few rows to confirm
print(data.head())
