import os
import json
import csv
import argparse

def parse_json_file(file_path):
    results = {}

    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return results
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        try:
            data = json.load(file)
            # If the data is a list, get the first element
            if isinstance(data, list):
                data = data[0]

            attributes = data.get('data', {}).get('attributes', {})
            av_results = attributes.get('results', {})
            
            file_paths = file_path.split(os.sep)
            
                
            package = file_paths[-1]
                            
            results['package'] = package[:-5] # Remove .json extension
            results['dataset'] = "typo-rust"
            results['av_results'] = av_results if isinstance(av_results, dict) else {}
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON file {file_path}: {e}")
        except Exception as e:
            print(f"Unexpected error processing file {file_path}: {e}")

    return results

def save_results_to_csv(results, output_file):
    # Collect all AV names
    av_names = set()
    for result in results:
        av_names.update(result['av_results'].keys())
    av_names = sorted(av_names)
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Package', 'Dataset', '#AVs'] + av_names
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for result in results:
            row = {
                'Package': result['package'],
                'Dataset': result['dataset'],
            }
            number_of_flaged_avs = 0
            for av in av_names:
                flaged_av = result.get('av_results', {}).get(av, {}).get('category', 'undetected')
                if flaged_av in ['malicious', 'suspicious']:
                    number_of_flaged_avs += 1
                    row[av] = 1                
                else:
                    row[av] = 0

            row['#AVs'] = number_of_flaged_avs
            writer.writerow(row)

def explore_and_parse_files(root_dir):
    results = []
    for root, dirs, files in os.walk(root_dir):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    result = parse_json_file(file_path)
                    if result:
                        results.append(result)
    return results

def main():
    parser = argparse.ArgumentParser(description="Parse bincapz scan results and save to CSV.")
    parser.add_argument('-i', '--input', type=str, required=True, help='Directory containing bincapz scan results.')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output CSV file path.')
    
    args = parser.parse_args()
    
    results_dir = os.path.abspath(args.input)
    output_file = os.path.abspath(args.output)
    results = explore_and_parse_files(results_dir)
    save_results_to_csv(results, output_file)

if __name__ == "__main__":
    main()