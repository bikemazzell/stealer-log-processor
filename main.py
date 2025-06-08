import argparse
import os
import sys
from processes.password_process import process_passwords_in_folder
from processes.autofill_process import process_autofills_in_folder

def main(root_folder, verbose):
    process_passwords_in_folder(root_folder, 'credentials.csv', verbose)
    process_autofills_in_folder(root_folder, 'autofills.csv', verbose)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Stealer Log Processor by @shoewind1997')
    parser.add_argument('root_folder', type=str, help='The root folder path to process.')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output.')

    args = parser.parse_args()

    if not os.path.isdir(args.root_folder):
        print(f"Error: {args.root_folder} is not a valid directory.")
        sys.exit(1)

    main(args.root_folder, args.verbose)
