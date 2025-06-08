import os
import concurrent.futures

def _extract_autofill_pairs_from_file(file_path, verbose=False):
    """Extracts form/value pairs from a single file."""
    if verbose:
        print(f"Processing {file_path}")
    
    form_value_pairs = set()
    try:
        with open(file_path, 'rb') as file:
            current_key = None
            for line in file:
                try:
                    decoded_line = line.decode('utf-8').strip()
                except UnicodeDecodeError:
                    if verbose:
                        print(f"Skipping undecodable line in file {file_path}")
                    continue
                
                if not decoded_line:
                    continue

                # Check for tab-separated key/value pairs on the same line
                if '\t' in decoded_line:
                    key, value = decoded_line.split('\t', 1)
                    form_value_pairs.add(f"{key.strip()}:{value.strip()}")
                else:
                    # Process FORM/VALUE pairs across lines
                    line_lower = decoded_line.lower()
                    if line_lower.startswith(('form:', 'name:')):
                        current_key = decoded_line.split(':', 1)[1].strip()
                    elif line_lower.startswith('value:') and current_key:
                        value = decoded_line.split(':', 1)[1].strip()
                        form_value_pairs.add(f"{current_key}:{value}")
                        current_key = None # Reset for next pair
        return form_value_pairs
    except IOError as e:
        if verbose:
            print(f"Error processing file {file_path}: {e}")
        return set()

def process_autofills_in_folder(root_folder, autofill_file_name, verbose=False):
    """
    Processes all autofill files in parallel, extracts key-value pairs,
    and saves them to a single combined file.
    """
    print(f"Processing autofills in folder: {root_folder}")

    files_to_process = []
    for root, _, files in os.walk(root_folder):
        autofill_directory = 'autofill' in os.path.basename(root).lower()
        for file_name in files:
            if autofill_directory or 'autofill' in file_name.lower():
                if file_name.lower().endswith(('.csv', '.tsv', '.txt')):
                    files_to_process.append(os.path.join(root, file_name))

    all_pairs = set()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_file = {executor.submit(_extract_autofill_pairs_from_file, file_path, verbose): file_path for file_path in files_to_process}
        for future in concurrent.futures.as_completed(future_to_file):
            file_path = future_to_file[future]
            try:
                pairs_from_file = future.result()
                all_pairs.update(pairs_from_file)
            except Exception as exc:
                print(f'{file_path} generated an exception: {exc}')

    # Write combined autofill pairs to the target file
    target_file_path = os.path.join(root_folder, autofill_file_name)
    try:
        with open(target_file_path, 'w', encoding='utf-8') as target_file:
            for pair in sorted(list(all_pairs)):
                target_file.write(pair + '\n')
        if verbose:
            print(f"Wrote combined autofills to: {target_file_path}")
    except IOError as e:
        if verbose:
            print(f"Error writing to file {target_file_path}: {e}")
