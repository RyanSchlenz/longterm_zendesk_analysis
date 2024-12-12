import pandas as pd
import sys
import io

# Redirect stdout to handle UTF-8 encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Define paths for input and output CSV files
input_csv_file_path = 'filtered_subjects.csv'
output_csv_file_path = 'aggregated_data.csv'

# Load the CSV file into a DataFrame
df = pd.read_csv(input_csv_file_path)

# Data preprocessing
df['Product - Service Desk Tool'] = df['Product - Service Desk Tool'].astype(str).replace('nan', '').str.strip()
df['Ticket created - Day of month'] = df['Ticket created - Day of month'].astype(float).fillna(0).astype(int)
df['Ticket created - Month'] = df['Ticket created - Month'].astype(str).str.strip()

# Generate a synthetic 'Year' column if not present (assume current year)
if 'Ticket created - Year' not in df.columns:
    df['Ticket created - Year'] = pd.Timestamp.now().year

# Create a 'Date' column from day, month, and year columns
df['Date'] = df.apply(lambda row: f"{row['Ticket created - Month']}/{int(row['Ticket created - Day of month']):02d}/{int(row['Ticket created - Year'])}", axis=1)

# Replace month names with numerical values
month_mapping = {
    'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 'June': '06',
    'July': '07', 'August': '08', 'September': '09', 'October': '10', 'November': '11', 'December': '12'
}
df['Date'] = df['Date'].replace(month_mapping, regex=True)

# Convert the 'Date' column to datetime format and drop invalid dates
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y', errors='coerce')
df = df.dropna(subset=['Date'])
df['Date'] = df['Date'].dt.strftime('%m/%d/%Y')

# Ensure 'Tickets' column exists; if not, add a placeholder for counting
if 'Tickets' not in df.columns:
    df['Tickets'] = 1

# Group by 'Date' and 'Product - Service Desk Tool' to aggregate ticket counts
aggregated_df = df.groupby(['Date', 'Product - Service Desk Tool']).agg({'Tickets': 'sum'}).reset_index()
aggregated_df.rename(columns={'Tickets': 'Ticket Count'}, inplace=True)

# Insert blank rows and calculate daily totals
final_rows = []
for date, group in aggregated_df.groupby('Date'):
    # Append rows for each Product - Service Desk Tool
    final_rows.extend(group.to_dict('records'))
    # Append a row for the daily total
    daily_total = group['Ticket Count'].sum()
    final_rows.append({'Date': date, 'Product - Service Desk Tool': 'Daily Total', 'Ticket Count': round(daily_total, 1)})
    # Append a blank row for spacing
    final_rows.append({'Date': '', 'Product - Service Desk Tool': '', 'Ticket Count': ''})

# Calculate the total tickets per day
daily_totals = aggregated_df.groupby('Date')['Ticket Count'].sum()

# Calculate the overall monthly average tickets per day
overall_avg = round(daily_totals.mean(), 1)

# Calculate the average tickets per day for each Product - Service Desk Tool
tool_averages = (
    aggregated_df.groupby('Product - Service Desk Tool')['Ticket Count']
    .sum()
    .div(len(daily_totals))  # Divide by the total number of unique days
    .reset_index()
)
tool_averages.rename(columns={'Ticket Count': 'Average Tickets per Day'}, inplace=True)
tool_averages['Average Tickets per Day'] = tool_averages['Average Tickets per Day'].round(1)

# Prepare averages rows
averages_data = [
    {'Date': 'Averages', 'Product - Service Desk Tool': 'Overall Average', 'Ticket Count': overall_avg}
]
averages_data += [
    {'Date': 'Averages', 'Product - Service Desk Tool': row['Product - Service Desk Tool'], 'Ticket Count': row['Average Tickets per Day']}
    for _, row in tool_averages.iterrows()
]

# Create a DataFrame for averages
averages_df = pd.DataFrame(averages_data)

# Add a blank row after averages
blank_row = {'Date': '', 'Product - Service Desk Tool': '', 'Ticket Count': ''}
averages_df = pd.concat([averages_df, pd.DataFrame([blank_row])], ignore_index=True)

# Place averages at the top of the file
final_df = pd.concat([averages_df, pd.DataFrame(final_rows)], ignore_index=True)

# Convert Ticket Count to numeric where possible, keep as float
final_df['Ticket Count'] = pd.to_numeric(final_df['Ticket Count'], errors='coerce').fillna('')

# Save to CSV
final_df.to_csv(output_csv_file_path, index=False)

print("Aggregation complete. Results saved to", output_csv_file_path)
