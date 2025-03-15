import csv
import subprocess
import os
from tqdm import tqdm
import pandas as pd

# Đường dẫn đến thư mục chứa lệnh oss-download
oss_download_path = r"..\..\tools\OSSGadget-0.1.422\src\oss-download\bin\Debug\net8.0"

# Đường dẫn đến thư mục muốn lưu các gói đã tải về
download_directory = r"typosquating_candidates"

# Đường dẫn đến tệp CSV chứa danh sách các gói cần tải về
csv_file_path = r"..\typo-squatting\downloads_unique.csv"

# Đọc tệp CSV
list_of_packages = []

df = pd.read_csv(csv_file_path)
files = df['Name'].to_list()
# get all package names has len over than 1
list_of_packages = [name for name in files if len(name)]
# print(list_of_packages)



# Tạo thanh tiến trình với tổng số dòng là độ dài của reader
with tqdm(total=len(list_of_packages), ncols=70) as pbar:
    for row in list_of_packages:
        # Lấy tên gói và đường dẫn tải về
        package_name = row

        # Tạo lệnh oss-download
        command = f"oss-download.exe --extract --download-directory {download_directory} -c pkg:cargo/{package_name}"

        # Chạy lệnh oss-download
        subprocess.run(command, cwd=oss_download_path, shell=True)

        # Cập nhật thanh tiến trình
        pbar.update(1)