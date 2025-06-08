# Stealer Log Processor

A high-performance Python tool for processing and extracting credentials and autofill data from stealer logs. This tool is designed to help victims of credential theft to find their compromised data in an organized and efficient manner.

## Features

- **Parallel Processing**: Utilizes multi-threading for faster data extraction
- **Robust Parsing**: Handles malformed entries and incomplete credential sets
- **Deduplication**: Automatically removes duplicate entries
- **Unicode Support**: Handles various character encodings gracefully
- **Verbose Mode**: Optional detailed logging for debugging

## Usage

```bash
python3 main.py [--verbose] <root_folder_path>
```

### Arguments

- `root_folder_path`: Path to the root folder containing stealer logs
- `--verbose`: (Optional) Enable detailed logging output

## Data Processing Details

### Credential Extraction
- Processes files with `pass` in their name and extensions `.csv`, `.tsv`, or `.txt`
- Extracts credentials in the format: `URL`, `USERNAME`, `PASSWORD`
- Handles various credential formats:
  - `url:`, `user:`, `pass:` format
  - `url:`, `username:`, `password:` format
  - `url:`, `login:`, `password:` format
- Outputs deduplicated credentials to `credentials.csv` in `user,pass,url` format
- Maintains data integrity by preserving original values

### Autofill Data Extraction
- Processes files in Autofill folders or with `autofill` in their name
- Extracts form field names and their corresponding values
- Handles both tab-separated and line-by-line formats
- Supports various field name formats:
  - `form:`, `name:` for field names
  - `value:` for field values
- Outputs deduplicated pairs to `autofills.csv` in `form:value` format
- Removes whitespace and normalizes entries for better deduplication

## Performance Optimizations

- Multi-threaded file processing for faster execution
- In-memory deduplication to minimize disk I/O
- Efficient data structures for quick lookups
- Smart file discovery to minimize unnecessary processing

## Error Handling

- Gracefully handles:
  - Unicode decoding errors
  - File access issues
  - Malformed entries
  - Incomplete credential sets
- Continues processing even when individual files fail

## License

MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.