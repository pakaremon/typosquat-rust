import os
import json
import requests
import csv
import json
from tqdm import tqdm
from collections import Counter
import pandas as pd

'''
# Đường dẫn đến thư mục chứa các file .sarif
dir_path = r"..\typo-squatting\name-typo-squatting"
AverageTypos = 6
# Lấy danh sách tên từ các file .sarif
names = []
files = [f for f in os.listdir(dir_path) if f.endswith(".sarif")]
for filename in files:
    with open(os.path.join(dir_path, filename), 'r') as f:
        data = json.load(f)

        package_names = []
        for candidate in data['runs'][0]['results']:
            if candidate['message']['text'].startswith('Potential Squat candidate'):
                package_names.append(candidate['locations'][0]['physicalLocation']['address']['name'].split('/')[-1])

        # if len(package_names) > AverageTypos:
        #     count_top_downloaded_packages = Counter()
        #     for name in tqdm(package_names, desc="Processing names", unit="name"):
        #         response = requests.get(f"https://crates.io/api/v1/crates/{name}")
        #         data = json.loads(response.text)
        #         download_count = data['crate']['downloads']

        #         count_top_downloaded_packages[name] = download_count

        #     package_names = [k for k, v in count_top_downloaded_packages.most_common()]

        names.extend(package_names)
                

print(len(set(names)))
# # Tạo file CSV mới
with open('downloads.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Name", "Download Count"])  # Ghi tiêu đề cột
 
# # Lấy số lượng tải về từ crates.io và ghi vào file CSV
total_names = len(names)
for i, name in enumerate(tqdm(names, desc="Pocessing names", unit="name")):
    response = requests.get(f"https://crates.io/api/v1/crates/{name}")
    data = json.loads(response.text)
    download_count = data['crate']['downloads']
    with open('downloads.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([name, download_count])  # Ghi dữ liệu vào file CSV

'''

# # Đọc file CSV, sắp xếp theo số lượng tải về từ thấp đến cao, và ghi lại vào file CSV

df = pd.read_csv('downloads.csv')
df.drop_duplicates(subset=["Name"], keep='first', inplace=True)
downloads = df.values.tolist()
    
downloads.sort(key=lambda x: int(x[1]))
with open('downloads1.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Name", "Download Count"])  # Ghi lại tiêu đề cột
    for name, download_count in downloads:
        writer.writerow([name, download_count])  # Ghi lại dữ liệu đã sắp xếp