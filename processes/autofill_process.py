import os

def process_autofills_in_folder(root_folder, verbose=False):
    autofill_file_name = 'a_credentials.csv'
    seen_pairs = set()  # Initialize the set to track seen form/value pairs

    if verbose:
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
       with open(file_path, 'r', encoding='utf-8') as file:
        current_form = None  # Only used for FORM/VALUE pair files
        for line in file:
            line = line.strip()
            line_lower = line.lower() 

            # Check for tab-separated key/value pairs on the same line
            if '\t' in line:
                key, value = line.split('\t', 1)
                pair = f"{key}:{value}"
                if pair not in seen_pairs:
                    seen_pairs.add(pair)
                    form_value_pairs.append(pair)
            else:
                # Process FORM/VALUE pairs across lines
                if line_lower.startswith(('form:', 'name:')):
                    current_key = line.split(':', 1)[1].strip() 
                elif (line_lower.startswith(('value:', 'value:')) and current_key is not None):
                    current_value = line.split(':', 1)[1].strip()
                    pair = f"{current_key}:{current_value}"
                    if pair not in seen_pairs:
                        seen_pairs.add(pair)
                        form_value_pairs.append(pair)
                    current_form = None  # Reset for next FORM/VALUE pair

        if form_value_pairs:
            autofills_output = ','.join(form_value_pairs)
            return autofills_output
        return None
    
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

def combine_autofill_files(output_files, root_folder, output_file_name, verbose=False):
    combined_autofills = set(output_files)

    target_file_path = os.path.join(root_folder, output_file_name)
    with open(target_file_path, 'w', encoding='utf-8') as target_file:
        for autofill in combined_autofills:
            target_file.write(autofill + '\n')
    if verbose:
        print(f"Wrote combined autofills to: {target_file_path}")