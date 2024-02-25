import os
import sys
from processes.password_process import process_passwords_in_folder
from processes.autofill_process import process_autofills_in_folder

def main(root_folder, verbose):
    process_passwords_in_folder(root_folder, verbose)
    process_autofills_in_folder(root_folder, verbose)

if __name__ == "__main__":
    verbose = False  # Default to non-verbose output
    args = sys.argv[1:]
    
    if '--verbose' in args:
        verbose = True
        args.remove('--verbose')

    if len(args) != 1:
        print("Stealer Log Processor by @shoewind1997")
        print("Usage: python3 main.py [--verbose] <root_folder_path>")
        sys.exit(1)
    
    root_folder = args[0]
    if not os.path.isdir(root_folder):
        print(f"Error: {root_folder} is not a valid directory.")
        sys.exit(1)

    main(root_folder, verbose)
