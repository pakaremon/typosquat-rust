import os
import json
import csv
from collections import Counter
import argparse

FILE_TEXT_EXTENSION = [
    '.txt', '.md', '.rtf', '.csv', '.log', '.xml', 
    '.yaml', '.yml', '.ini', '.conf', '.cfg', 
    '.sql', '.tex', '.html', '.htm', '.srt', 'README', '.json', '.lock',
    '.toml.orig'
]

def parse_oss_detect_backdoor_file(file_path):
    file_parts = file_path.split(os.sep)
    package_information = {}

    package_information['package'] = file_parts[-1].removesuffix('.sarif')

    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            results = []
            for run in data.get('runs', []): # only have 1 row
                number_of_alert = Counter()
                for result in run.get('results', []):
                    for location in result.get('locations', []):
                        physical_location = location.get('physicalLocation', {})
                        file_name = physical_location.get('address', {}).get('fullyQualifiedName', 'Unknown')

                        # Check if file name does not end with specified extensions
                        if not file_name.endswith(tuple(FILE_TEXT_EXTENSION)) and file_name != 'Unknown':
                            number_of_alert[file_name] += 1
        
            for file_name, number_of_alerts in number_of_alert.items():
                if file_name.startswith('https://crates.io/crates'):
                    continue
                results.append({
                    'package': package_information['package'],
                    'file': file_name,
                    'number_of_alerts': number_of_alerts,
                })

            
            return results
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error processing file {file_path}: {e}")
        return []

def save_results_to_csv(results, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Package', 'File', 'Number of Alerts']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for result in results:
            writer.writerow({
                'Package': result['package'],
                'File': result['file'],
                'Number of Alerts': result['number_of_alerts'],
            })

def explore_and_parse_files(root_dir):
    """Return a list of results from parsing JSON files in the root directory."""
    all_results = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                results = parse_oss_detect_backdoor_file(file_path)
                all_results.extend(results)
    return all_results

def main():
    parser = argparse.ArgumentParser(description="Parse OSS Detect Backdoor scan results and save to CSV.")
    parser.add_argument('-i', '--input', type=str, required=True, help='Directory containing OSS Detect Backdoor scan results.')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output CSV file path.')
    
    args = parser.parse_args()

    root_dir = os.path.abspath(args.input)
    results = explore_and_parse_files(root_dir)
    
    output_file = os.path.abspath(args.output)
    save_results_to_csv(results, output_file)

if __name__ == "__main__":
    main()
