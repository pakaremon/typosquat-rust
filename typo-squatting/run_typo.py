import os
import subprocess
import shutil
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from threading import Lock

lock = Lock()
processing_names = set()

def run_command(name):
    dst = r'..\typo-squatting\name-typo-squatting\{0}.sarif'.format(name)
    with lock:
        if name in processing_names or os.path.exists(dst):
            pbar.update()  # Cập nhật thanh tiến trình
            print(f"File {name} already exists. Skipping.")
            return
        processing_names.add(name)
    command = r'..\..\tools\OSSGadget-0.1.422\src\oss-find-squats\bin\Debug\net8.0\oss-find-squats.exe -o {0} --format sarifv2 pkg:cargo/{1}'.format(dst, name)
    # print(f"Executing command for {command}.")
    result = subprocess.run(command, shell=True, capture_output=True)
    if result.returncode == 0:
        print(f"Command for {name} executed successfully.")
    else:
        print(f"Command for {name} failed with return code {result.returncode}.")
    pbar.update()  # Cập nhật thanh tiến trình

with open(r'top_packages.txt', 'r') as f:
    lines = [line.strip() for line in f]

pbar = tqdm(total=len(lines), desc="Processing ", unit="name")
with ThreadPoolExecutor() as executor:
    executor.map(run_command, lines)
pbar.close()