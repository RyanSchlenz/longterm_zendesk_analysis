import pandas as pd

def main():
    # Define the path to the CSV file
    input_csv_file_path = 'ticket_data.csv'
    output_csv_file_path = 'cleaned_data.csv'

    # Load the CSV file into a DataFrame
    df = pd.read_csv(input_csv_file_path)

    # Ensure 'Ticket subject' column is treated as a string
    df['Ticket subject'] = df['Ticket subject'].astype(str)

    # Define the unwanted patterns without periods
    unwanted_patterns = [
        r'\bTermination-\b.*',
        r'\bCreate HCHB\b.*',
        r'\bCreate desktop\b.*',
        r'\bCreate Forcura\b.*',
        r'\bVerify System\b.*',
        r'\bCompleted: Complete with DocuSign\b.*',
        r'\bBackground Check\b.*',
        r'\bCompleted With Errors\b.*',
        r'\bAlert: Network\b.*',
        r'\bReset: Facility\b.*',
        r'\bFax Status for Job\b.*',
        r'\bAssign Online Learning Hub\b.*',
        r'\bCall with Caller\b.*',
        r'\bSUPPORT EXPIRED\b.*',
        r'\bADP\b.*',
        r'\bA Rehire Has Been Processed\b.*',
        r'\bMissed call with Caller\b.*',
        r'\bHartford Inbound\b.*',
        r'\bMissed call from\b.*',
        r'\bwithholding\b.*',
        r'\bCall Back Request\b.*',
        r'\bCall on\b.*',
        r'\bCall with\b.*',
        r'\bUnknown caller\b.*',
        r'\bVoicemail\b.*',
        r'\bvoicemail\b.*',
        r'\bConversation with\b.*'
        r'\b"Conversation with\b.*',
        r'\bConversation with \b.*',
        r'\bCall Back - No Answer\b.*',
        r'\bCall back follow-up\b.*',
        r'\bCall back request\b.*',
        r'\bCall back\b.*', 
        r'\bCallback\b.*',
        r'\bAbandoned Call\b.*', 
        r'\bCall back\b.*', 
        r'\bYour VM Pin has been reset\b.*'
    ]

    # Debug: Print original 'Ticket subject' values to see which ones are being missed
    print("Original 'Ticket subject' values:")
    print(df['Ticket subject'].head(20))

    # Filter out rows where 'Ticket subject' contains any of the unwanted patterns
    for pattern in unwanted_patterns:
        # Debug: Print the pattern being used
        print(f"Applying pattern: {pattern}")
        df_filtered = df[~df['Ticket subject'].str.contains(pattern, regex=True, na=False)]

        # Debug: Print number of rows before and after filtering
        print(f"Number of rows before filtering with pattern '{pattern}': {len(df)}")
        print(f"Number of rows after filtering with pattern '{pattern}': {len(df_filtered)}")

        df = df_filtered.copy()  # Update df to be the filtered result

    # Debug: Check unique values in 'Ticket subject' to ensure unwanted patterns are removed
    print("Unique 'Ticket subject' values after unwanted patterns removal:")
    try:
        # Convert to string and handle encoding issues
        unique_values = df['Ticket subject'].unique()
        print([str(value).encode('utf-8', errors='replace').decode('utf-8') for value in unique_values])
    except UnicodeEncodeError:
        print("Encoding error encountered while printing unique values.")

    # Filter rows where 'Tickets' column contains a number
    df_filtered = df[df['Tickets'].astype(str).str.contains(r'\d+', regex=True)]

    # Define the allowed ticket groups
    allowed_ticket_groups = [
        'IT', 'Equipment', 'Fuze', 'Hartford Inbound', 'Hartford Outbound',
        'Hartford UAP', 'Light Agents', 'Network', 'Mobile Reconciliation',
        'Outbound', 'Tier 1', 'Tier 2', 'UAP', 'Tier 1 - OB', 'Trainee', 'Equipment Waiting', 'Email', 'Inbound', 'QA'
    ]

    # Debug: Check unique values in 'Ticket group' before filtering
    print("Unique 'Ticket group' values before filtering:")
    print(df_filtered['Ticket group'].unique())

    # Filter rows where 'Ticket group' is in the allowed list
    df_filtered = df_filtered[df_filtered['Ticket group'].isin(allowed_ticket_groups)]

    # Debug: Check unique values in 'Ticket group' after filtering
    print("Unique 'Ticket group' values after filtering:")
    print(df_filtered['Ticket group'].unique())

    # Save the filtered DataFrame to a new CSV file
    df_filtered.to_csv(output_csv_file_path, index=False)

    print(f"Filtered CSV file saved to {output_csv_file_path}")

if __name__ == "__main__":
    main()
