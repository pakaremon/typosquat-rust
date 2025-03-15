import json
import os
import csv
import argparse

input_dir = r"./Typosquatting_attacks_on_the_Rust_ecosystem\packages\detect\results\package_analysis"




def parse_oss_detect_backdoor_file(input_dir):
    report = {
        'unique_commands': set(), 
        'unique_domains': set(),
        'unique_ips': set(),

    }
    
    for file in os.listdir(input_dir):
        if file.endswith(".json"):
            file_path = os.path.join(input_dir, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for section in ['install', 'import']:
                    if section in data['Analysis']:
                        dns_list = data['Analysis'][section].get('DNS', [])
                        if dns_list:
                            for dns in dns_list:
                                if dns:
                                    for hostname in dns.get('Queries', []):
                                        report['unique_domains'].add(hostname.get('Hostname', ''))


                        socket_list = data['Analysis'][section].get('Sockets', [])
                        if socket_list:
                            for socket in socket_list:
                                if socket:
                                    # ip_address = socket.get('Address', '')
                                    # report['unique_ips'].add(ip_address)
                                    hostname = socket.get('Hostname', '')
                                    report['unique_domains'].add(hostname)
                        
                        command_list = data['Analysis'][section].get('Environment', [])
                        if command_list:
                            for command in command_list:
                                if command:
                                    report['unique_commands'].add(' '.join(command.get('Command', [])))

    return report
                        








def main():
    report = parse_oss_detect_backdoor_file(input_dir)
    # Convert sets to lists for JSON serialization
    report_serializable = {
        'unique_commands': list(report['unique_commands']),
        'unique_domains': list(report['unique_domains']),
        'unique_ips': list(report['unique_ips']),
    }
    with open('report.json', 'w') as f:
        json.dump(report_serializable, f, indent=4)



if __name__ == '__main__':
    main()