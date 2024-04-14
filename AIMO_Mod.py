import pandas as pd

# Load the DataFrame from the CSV file
df = pd.read_csv('AIME_Problems_and_Answers.csv')

# Filter the DataFrame to include only rows where "Question" contains "Solution"
filtered_df = df[df['Question'].str.contains("Solution")]

# Remove the word "Solution" from the "Question" column
filtered_df['Question'] = filtered_df['Question'].str.replace("Solution", "", regex=True)

# Save the filtered DataFrame to a new CSV file
filtered_df.to_csv('Filtered_AIME_Problems_and_Answers.csv', index=False)

print("Filtered and cleaned DataFrame saved to 'Filtered_AIME_Problems_and_Answers.csv'.")
