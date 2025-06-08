import os
import concurrent.futures

def _extract_passwords_from_file(file_path, verbose=False):
    """Extracts credentials from a single file, assuming a URL, User, Pass sequence."""
    if verbose:
        print(f"Processing {file_path}")
    credentials = set()
    password_info = {}

    try:
        with open(file_path, 'rb') as file:
            for line in file:
                try:
                    decoded_line = line.decode('utf-8').strip()
                except UnicodeDecodeError:
                    if verbose:
                        print(f"Skipping undecodable line in file {file_path}")
                    continue

                line_lower = decoded_line.lower()

                # A 'URL' line always starts a new credential entry.
                if 'url:' in line_lower:
                    password_info = {}  # Reset for a new entry
                    parts = decoded_line.split(':', 1)
                    if len(parts) == 2:
                        password_info['URL'] = parts[1].strip()
                elif 'user:' in line_lower or 'username:' in line_lower or 'login:' in line_lower:
                    if 'URL' in password_info:
                        parts = decoded_line.split(':', 1)
                        if len(parts) == 2:
                            password_info['USER'] = parts[1].strip()
                elif 'pass:' in line_lower or 'password:' in line_lower:
                    if 'URL' in password_info and 'USER' in password_info:
                        parts = decoded_line.split(':', 1)
                        if len(parts) == 2:
                            password_info['PASS'] = parts[1].strip()
                            credentials.add((password_info['USER'], password_info['PASS'], password_info['URL']))
                            password_info = {}  # Reset after successful extraction
    except IOError as e:
        print(f"Error processing file {file_path}: {e}")
    
    return credentials

def process_passwords_in_folder(root_folder, password_file_name, verbose=False):
    """
    Processes all password files in parallel, extracts credentials,
    and saves them to a single combined file.
    """
    print(f"Processing passwords in folder: {root_folder}")

    files_to_process = []
    for root, _, files in os.walk(root_folder):
        for file_name in files:
            if file_name.lower().endswith(('.csv', '.tsv', '.txt')) and 'password' in file_name.lower():
                files_to_process.append(os.path.join(root, file_name))

    all_credentials = set()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_file = {executor.submit(_extract_passwords_from_file, file, verbose): file for file in files_to_process}
        for future in concurrent.futures.as_completed(future_to_file):
            file_path = future_to_file[future]
            try:
                credentials_from_file = future.result()
                all_credentials.update(credentials_from_file)
            except Exception as exc:
                print(f'{file_path} generated an exception: {exc}')

    # Write combined credentials to the target file
    target_file_path = os.path.join(root_folder, password_file_name)
    try:
        with open(target_file_path, 'w', encoding='utf-8') as target_file:
            # Sort for deterministic output
            for user, pwd, url in sorted(list(all_credentials)):
                target_file.write(f"{user},{pwd},{url}\n")
        if verbose:
            print(f"Wrote combined credentials to: {target_file_path}")
    except IOError as e:
        if verbose:
            print(f"Error writing to file {target_file_path}: {e}")

    