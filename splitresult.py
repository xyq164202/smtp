import pandas as pd

def split_emails_into_files(excel_path, column_name, output_folder, group_size=40):
    # Load the Excel file
    df = pd.read_excel(excel_path)
    
    # Extract email addresses
    emails = df[column_name].dropna().unique()
    
    # Split into groups
    email_groups = [emails[i:i + group_size] for i in range(0, len(emails), group_size)]
    
    # Save each group to a separate text file
    for idx, group in enumerate(email_groups, start=1):
        file_path = f"{output_folder}/email_group_{idx}.txt"
        with open(file_path, 'w') as file:
            for email in group:
                file.write(f"{email}\n")
        print(f"Saved {len(group)} emails to {file_path}")

# Example usage
excel_path = '/Users/qinyaoxu/Downloads/company swag.xlsx'
column_name = '邮箱/电话/skype'
output_folder = '/Users/qinyaoxu/Downloads/split'

split_emails_into_files(excel_path, column_name, output_folder)
