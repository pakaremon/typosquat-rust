import os
import json

def count(directory):
    files = [f for f in os.listdir(directory) if f.endswith('.sarif')]
    total_typo_alerts = 0

    for file in files:
        with open(os.path.join(directory, file), 'r') as json_file:
            data = json.load(json_file)
            alerts = 0
            for candiate in data['runs'][0]['results']:
                if candiate['message']['text'].startswith('Potential Squat candidate'):
                    alerts += 1


            total_typo_alerts += alerts
         

    average = round(total_typo_alerts / len(files)) if files else 0

    

    return average

directory = r'..\typo-squatting\name-typo-squatting' 

average_typo = count(directory)
print(f'Average number of typo alerts per package: {average_typo}')
