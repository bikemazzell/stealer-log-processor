# Stealer Log Processor
by @shoewind1997

Process Stealer Log folders to extract essential parts in an organized way

## Usage

`python3 main.py [--verbose] <root_folder_path>`

## Details

- Extracts credentials from any files that have `pass` in their name and an extension of `csv`, `tsv`, or `txt`
    - Outputs all credentials to `p_credentials.csv` in `user,pass,url` format
    - Removes duplicates on each folder level