import os

def process_passwords_in_folder(root_folder, verbose=False):
    password_file_name = 'p_credentials.csv'

    print(f"Processing passwords in folder: {root_folder}")

    # Initialize list to store paths of output files in subfolders
    output_files = []

    # Traverse through each subfolder
    subfolders = [f.path for f in os.scandir(root_folder) if f.is_dir()]
    for subfolder in subfolders:
        output_file_path = process_passwords_in_subfolder(subfolder, verbose)
        output_files.append(output_file_path)

    # Combine all output files into one at root_folder level
    combine_password_files(output_files, root_folder, password_file_name, verbose)

def process_passwords_in_subfolder(subfolder, verbose=False):
    password_file_name = 'p_credentials.csv'
    
    if verbose:
        print(f"\tsubfolder: {subfolder}")

    # Initialize list to store credentials
    credentials = []

    # Traverse through files in subfolder
    for root, _, files in os.walk(subfolder):
        for file_name in files:
            # Check if the file has a valid extension
            if file_name.lower().endswith(('.csv', '.tsv', '.txt')) and file_name.lower().find('password') != -1:
                process_password_files(os.path.join(root, file_name), credentials, verbose)

    # Write credentials to the output file in subfolder
    output_file_path = os.path.join(subfolder, password_file_name)
    with open(output_file_path, 'w', encoding='utf-8') as out_file:
        for credential in credentials:
            out_file.write(','.join(credential) + '\n')

    return output_file_path

def process_password_files(file_path, credentials, verbose=False):
    if verbose:
        print(f"Processing {file_path}")
    password_info = {'URL': '', 'USER': '', 'PASS': ''}
    expected_next = 'URL'  # Start expecting a URL

    try:    
        with open(file_path, 'rb') as file:
            for line in file:
                try:
                    decoded_line = line.decode('utf-8').strip()
                except UnicodeDecodeError:
                    if verbose:
                        print(f"Skipping undecodable line in file {file_path}")
                    continue

                 # Skip lines that do not start with expected credential keys
                if not (decoded_line.lower().startswith('url:') or 
                    decoded_line.lower().startswith('user:') or 
                    decoded_line.lower().startswith('login:') or 
                    decoded_line.lower().startswith('pass:') or 
                    decoded_line.lower().startswith('password:')):
                    continue

                line_lower = decoded_line.lower()
                 # Process line if it starts with expected info and matches the expected sequence
                if expected_next == 'URL' and 'url:' in line_lower:
                    parts = decoded_line.split(':', 1)
                    if len(parts) == 2:
                        password_info['URL'] = parts[1].strip()
                        expected_next = 'USER'  # Next, expect User/Login

                elif expected_next == 'USER' and ('user:' in line_lower or 'login:' in line_lower):
                    parts = decoded_line.split(':', 1)
                    if len(parts) == 2:
                        password_info['USER'] = parts[1].strip()
                        expected_next = 'PASS'  # Next, expect Password

                elif expected_next == 'PASS' and ('pass:' in line_lower or 'password:' in line_lower):
                    parts = decoded_line.split(':', 1)
                    if len(parts) == 2:
                        password_info['PASS'] = parts[1].strip()
                        # After capturing Password, append the set to credentials and reset
                        credentials.append((password_info['USER'], password_info['PASS'], password_info['URL']))
                        password_info = {'URL': '', 'USER': '', 'PASS': ''}  # Reset for next credential set
                        expected_next = 'URL'  # Start expecting a URL again for the next set
                        
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

def combine_password_files(output_files, root_folder, output_file_name, verbose=False):
    # Collect all credentials from output files
    combined_credentials = set()
    for output_file in output_files:
        with open(output_file, 'r', encoding='utf-8') as file:
            for line in file:
                combined_credentials.add(line.strip())

    # Write combined credentials to the target file
    target_file_path = os.path.join(root_folder, output_file_name)
    with open(target_file_path, 'w', encoding='utf-8') as target_file:
        for credential in combined_credentials:
            target_file.write(credential + '\n')
    if verbose:
        print(f"Wrote combined credentials to: {target_file_path}")

     # Clean up intermediate p_credentials.csv files from subfolders
    for output_file in output_files:
            os.remove(output_file)