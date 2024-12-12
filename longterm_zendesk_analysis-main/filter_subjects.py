import pandas as pd
import re

def main():
    # Define the paths for the input and output CSV files
    input_csv_file_path = 'filtered_groups.csv'
    output_csv_file_path = 'filtered_subjects.csv'

    # Define keyword rules for specific Subject Groups using regex
    keyword_rules = {
        'ADUC': [
            r'.*\bactive directory\b.*', r'.*\baduc\b.*', 
            r'.*\bDisable Accounts\b.*', r'.*\bAD\b.*'
        ],
        'Azure Virtual Desktop (AVD)': [
            r'.*\bavd\b.*', r'.*\bremote desktop\b.*', r'.*\bazure virtual desktop\b.*', 
            r'.*\bpennant desktop\b.*', r'.*\bremote desk top\b.*', r'.*\bAzure Access\b.*', 
            r'.*\baccess to azure\b.*', r'.*\bazure\b.*', r'.*\bADV\b.*'
        ],
        'Workday': [
            r'.*\bworker profile update\b.*', r'.*\bprofile update\b.*', r'.*\bupdated withholding\b.*'
        ],
        'HCHB': [
            r'.*\bhchb\b.*', r'.*\bpointcare training\b.*', r'.*\bpointcare\b.*', 
            r'.*\bpoint care\b.*', r'.*\bPoint Care\b.*', r'.*\bPointCare\b.*',
            r'.*\bhome care home base\b.*', r'.*\bhomecarehomebase\b.*', 
            r'.*\bworkflow\b.*', r'.*\bHCHB\b.*', r'.*\bhomecare homebase\b.*', 
            r'.*\bPennant Guide\b.*', r'.*\bPennantGuide\b.*'
        ],
        'Printer/Scanner/Copier': [
            r'.*\bprinter\b.*', r'.*\bscanner\b.*', r'.*\bcopier\b.*', 
            r'.*\badd printer\b.*', r'.*\bprinterlogic\b.*', 
            r'.*\badd new printer\b.*', r'.*\bremove printer\b.*'
        ],
        'Drive Access': [
            r'.*\bj-drive\b.*', r'.*\bg-drive\b.*', r'.*\bg drive\b.*', 
            r'.*\bshared drive\b.*', r'.*\bh-drive\b.*', r'.*\bH Drive\b.*', 
            r'.*\bh drive\b.*', r'.*\baccess to drive\b.*', r'.*\bnetwork drive\b.*', 
            r'.*\bunable to access drive\b.*', r'.*\bdrive connection issue\b.*', 
            r'.*\bsyncing\b.*', r'.*\bSyncing\b.*', r'.*\bsync\b.*', r'.*\bSync\b.*'
        ],
        'Exchange': [
            r'.*\bemail\b.*', r'.*\bmail\b.*', r'.*\bmailbox\b.*', 
            r'.*\bemail inbox\b.*', r'.*\binbox\b.*', 
            r'.*\bdistribution list\b.*', r'.*\bdl\b.*', 
            r'.*\bshared mailbox\b.*', r'.*\boutlook\b.*', r'.*\bGroup List\b.*'
        ],
        'Faxage': [
            r'.*\bfax\b.*', r'.*\bfaxage\b.*', r'.*\bfaxes\b.*', 
            r'.*\bfaxs\b.*', r'.*\bfaxages\b.*', r'.*\bfax age\b.*'  
        ],
        'MOBI': [
            r'.*\bmobi\b.*', r'.*\bmobile\b.*', r'.*\bcellphone\b.*', 
            r'.*\bcell\b.*', r'.*\bphone\b.*', r'.*\bphone number\b.*', 
            r'.*\bsamsung\b.*', r'.*\bandroid\b.*', r'.*\bverizon\b.*', 
            r'.*\bactivate\b.*', r'.*\bphones\b.*', r'.*\bHotspot\b.*', 
            r'.*\bBluetooth\b.*', r'.*\btiger\b.*', r'.*\bTiger\b.*', 
            r'.*\bhotspot\b.*', r'.*\bhot spot\b.*', r'.*\bText Message\b.*', 
            r'.*\btext message\b.*', r'.*\btextmessage\b.*'
        ],
        'PCC': [
            r'.*\bpcc\b.*', r'.*\bpointclickcare\b.*', r'.*\bpoint click care\b.*', 
            r'.*\bPCC\b.*'
        ],
        'Fuze': [
            r'.*\bfuze\b.*'
        ],
        'Equipment': [
            r'.*\bshipping label\b.*', r'.*\bequipment order\b.*', 
            r'.*\border equipment\b.*', r'.*\bFedEx\b.*', r'.*\blaptops\b.*', 
            r'.*\blaptop\b.*', r'.*\bcomputer\b.*', r'.*\bchromebook\b.*', 
            r'.*\bchrome book\b.*', r'.*\bntd\b.*', r'.*\bstratodesk\b.*', 
            r'.*\bstrato desk\b.*', r'.*\btablet\b.*', r'.*\breturn label\b.*', 
            r'.*\bHP\b.*', r'.*\bMonitor\b.*', r'.*\bDevice\b.*', 
            r'.*\bdevice\b.*', r'.*\bHeadphone\b.*', r'.*\bheadphone\b.*', 
            r'.*\bMicrophone\b.*', r'.*\bmicrophone\b.*'
        ],
        'UAP': [
            r'.*\bUAP\b.*', r'.*\buser account provisioning\b.*', 
            r'.*\btermination\b.*', r'.*\btermination-\b.*', r'.*\btermed\b.*', 
            r'.*\bTerminations\b.*', r'.*\bname change\b.*', r'.*\bName Change\b.*', 
            r'.*\bName change\b.*'
        ],
        'Microsoft 365 Products': [
            r'.*\bExcel\b.*', r'.*\bTeams\b.*', r'.*\bteams\b.*', 
            r'.*\bexcel\b.*'
        ],
        'Adobe': [
            r'.*\badobe\b.*', r'.*\bAdobe\b.*', r'.*\badobe pdf\b.*'
        ],
        'Forcura': [
            r'.*\bforcura\b.*', r'.*\bForcura\b.*'
        ],
        'Network': [
            r'.*\bservice alert\b.*', r'.*\bnetwork\b.*', r'.*\binternet\b.*', 
            r'.*\bfirewall\b.*', r'.*\bISP\b.*', r'.*\byour service is restored\b.*'  
        ],
        'Smartsheet': [
            r'.*\bsmartsheet\b.*', r'.*\bsmartsheets\b.*', 
            r'.*\bsmart sheet\b.*', r'.*\bsmart sheets\b.*'
        ],
        'Pennant Guide': [
            r'.*\bPennU\b.*', r'.*\bPenn U\b.*', r'.*\bPennant U\b.*', 
            r'.*\bPennant University\b.*', r'.*\bPennantUniversity\b.*', 
            r'.*\bPennant Guide\b.*', r'.*\bPennantGuide\b.*', 
            r'.*\bPenn Guide\b.*', r'.*\bhartfordguide\b.*', r'.*\bhartford guide\b.*'
        ],
        'End User Training': [
            r'.*\bMissed Call Follow Up\b.*', r'.*\bhelp\b.*', 
            r'.*\bCall Back Request\b.*', r'.*\bhelp please\b.*', 
            r'.*\burgent\b.*', r'.*\bNo vm left\b.*', r'.*\bno vm\b.*', 
            r'.*\bUnknown caller\b.*', r'.*\bConversation with\b.*',  
            r'.*\bfollow up\b.*', r'.*\bDocuSign\b.*', r'.*\bVoicemail\b.*', 
            r'.*\bvoicemail\b.*'
        ],
        'Zendesk': [
            r'.*\bZenDesk\b.*', r'.*\bZendesk\b.*', r'.*\bzendesk\b.*', 
            r'.*\bZen Desk\b.*'
        ],
        'SSO Password Reset': [
            r'.*\bsso\b.*', r'.*\bsingle sign-on\b.*', r'.*\blogin\b.*', 
            r'.*\bcannot login\b.*', r'.*\blogin issue\b.*', 
            r'.*\blogins\b.*', r'.*\blog ins\b.*', r'.*\bcreds check\b.*', 
            r'.*\bpassword reset\b.*', r'.*\bpw reset\b.*', r'.*\bpw\b.*', 
            r'.*\bcredential\b.*', r'.*\bcredentials\b.*', r'.*\bSSO\b.*', 
            r'.*\breset\b.*', r'.*\breset password\b.*', r'.*\bWorkday login\b.*', 
            r'.*\bworkday login\b.*', r'.*\bWorkday Login\b.*'
        ]
    }

    # Load the CSV file into a DataFrame
    df = pd.read_csv(input_csv_file_path)

    # Ensure relevant columns are treated as strings
    df['Ticket subject'] = df['Ticket subject'].astype(str)

    # Create a new column for ticket categorization based on keyword rules
    df['Ticket Category'] = 'Uncategorized'  # Default category

    # Iterate through the keyword rules and categorize tickets
    for category, patterns in keyword_rules.items():
        combined_pattern = '|'.join(patterns)
        matches = df['Ticket subject'].str.contains(combined_pattern, case=False, na=False)
        df.loc[matches, 'Ticket Category'] = category

    # Replace Product - Service Desk Tool with Ticket Category by default
    df['Product - Service Desk Tool'] = df['Ticket Category']

    # Override Product - Service Desk Tool with "Equipment" when Ticket group is "Equipment" or "Equipment Waiting"
    equipment_condition = df['Ticket group'].isin(['Equipment', 'Equipment Waiting'])
    df.loc[equipment_condition, 'Product - Service Desk Tool'] = 'Equipment'

    # Loop through the DataFrame and apply the changes based on conditions
    for index, row in df.iterrows():
        ticket_group = row['Ticket group']

        # Condition to change Product - Service Desk Tool and Ticket Category based on Ticket group
        if ticket_group == 'UAP':
            df.at[index, 'Product - Service Desk Tool'] = 'UAP'
            df.at[index, 'Ticket Category'] = 'UAP'

    # Filter the DataFrame for tickets that are categorized
    categorized_tickets = df[df['Ticket Category'] != 'Uncategorized']

    # Save the categorized tickets to a new CSV file
    categorized_tickets.to_csv(output_csv_file_path, index=False)

if __name__ == '__main__':
    main()