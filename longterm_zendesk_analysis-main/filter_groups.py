import pandas as pd

def main():
    # Define the paths for the input and output CSV files
    input_csv_file_path = 'cleaned_data.csv'
    output_csv_file_path = 'filtered_groups.csv'

    # Load the CSV file into a DataFrame
    df = pd.read_csv(input_csv_file_path)

    # Ensure relevant columns are treated as strings
    df['Ticket group'] = df['Ticket group'].astype(str)
    df['Product - Service Desk Tool'] = df['Product - Service Desk Tool'].astype(str)

    # Update 'Product - Service Desk Tool' based on 'Ticket group'
    df.loc[df['Ticket group'].isin(['Equipment', 'Equipment Waiting']), 'Product - Service Desk Tool'] = 'Equipment'
    df.loc[df['Ticket group'] == 'Fuze', 'Product - Service Desk Tool'] = 'Fuze'
    df.loc[df['Ticket group'].isin(['Hartford UAP', 'UAP']), 'Product - Service Desk Tool'] = 'UAP'
    df.loc[df['Ticket group'] == 'Network', 'Product - Service Desk Tool'] = 'Network'
    df.loc[df['Ticket group'] == 'Email', 'Product - Service Desk Tool'] = 'Exchange'
    
    # Save the updated DataFrame to a new CSV file
    df.to_csv(output_csv_file_path, index=False)

    print(f"Filtered Groups CSV file saved to {output_csv_file_path}")

if __name__ == "__main__":
    main()
