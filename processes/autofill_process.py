import os

def process_autofills_in_folder(root_folder, autofill_file_name, verbose=False):
    seen_pairs = set()  # Initialize the set to track seen form/value pairs

    print(f"Processing autofills in folder: {root_folder}")

    output_files = []

    for root, dirs, files in os.walk(root_folder):
        autofill_directory = 'autofill' in os.path.basename(root).lower()
        for file_name in files:
            if autofill_directory or 'autofill' in file_name.lower():
                if file_name.lower().endswith(('.csv', '.tsv', '.txt')):
                    file_path = os.path.join(root, file_name)
                    output_file_path = process_autofill_files(file_path, seen_pairs, verbose)
                    if output_file_path: 
                        output_files.append(output_file_path)

    combine_autofill_files(output_files, root_folder, autofill_file_name, verbose)

def process_autofill_files(file_path, seen_pairs, verbose=False):
    if verbose:
        print(f"Processing {file_path}")
    form_value_pairs = []
    
    try:
        with open(file_path, 'rb') as file:
            current_key = None  # Use current_key instead of current_form
            
            for line in file:
                try:
                    decoded_line = line.decode('utf-8').strip()
                except UnicodeDecodeError:
                    if verbose:
                        print(f"Skipping undecodable line in file {file_path}")
                    continue
                
                line_lower = decoded_line.lower()

                # Check for tab-separated key/value pairs on the same line
                if '\t' in decoded_line:
                    key, value = decoded_line.split('\t', 1)
                    pair = f"{key}:{value}"
                    if pair not in seen_pairs:
                        seen_pairs.add(pair)
                        form_value_pairs.append(pair)
                else:
                    # Process FORM/VALUE pairs across lines
                    if line_lower.startswith(('form:', 'name:')):
                        current_key = decoded_line.split(':', 1)[1].strip()
                    elif (line_lower.startswith(('value:')) and current_key is not None):
                        current_value = decoded_line.split(':', 1)[1].strip()
                        pair = f"{current_key}:{current_value}"
                        if pair not in seen_pairs:
                            seen_pairs.add(pair)
                            form_value_pairs.append(pair)
                        current_key = None  # Reset for next FORM/VALUE pair

        if form_value_pairs:
            autofills_output = ','.join(form_value_pairs)
            return autofills_output
        return None

    except IOError as e:
        if verbose:
            print(f"Error processing file {file_path}: {e}")

def combine_autofill_files(output_files, root_folder, output_file_name, verbose=False):
    if verbose:
        print(f"Combining output files into {output_file_name}")

    target_file_path = os.path.join(root_folder, output_file_name)
    try:
        with open(target_file_path, 'w', encoding='utf-8') as target_file:
            for autofill in set(output_files):
                target_file.write(autofill + '\n')
        if verbose:
            print(f"Wrote combined autofills to: {target_file_path}")
     
    except IOError as e:
        if verbose:
            print(f"Error writing to file {target_file_path}: {e}")
