import os
import subprocess
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

# Thread-safe global variables
lock = Lock()
processing_names = set()

# Input and output paths
input_file = r"D:\HocTap\projectDrVuDucLy\Typosquatting_attacks_on_the_Rust_ecosystem\packages\typo-squatting\downloads_unique.csv"
output_dir = r"D:\HocTap\projectDrVuDucLy\Typosquatting_attacks_on_the_Rust_ecosystem\packages\detect\results\odb_full"
oss_detect_backdoor_path = r"D:\HocTap\projectDrVuDucLy\tools\OSSGadget-0.1.422\src\oss-detect-backdoor\bin\Debug\net8.0\oss-detect-backdoor.exe"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)


def run_odb(name):
    """Runs oss-detect-backdoor for a given package name."""
    output_file = os.path.join(output_dir, f"{name}.sarif")

    with lock:
        if name in processing_names or os.path.exists(output_file):
            pbar.update()  # Safely update progress bar
            print(f"File {name} already exists. Skipping.")
            return
        processing_names.add(name)

    # Build command using list format (safer than shell=True)
    command = [oss_detect_backdoor_path, "-f", "sarifv2", f"pkg:cargo/{name}", "-o", output_file]

    try:
        # print(command)
        result = subprocess.run(command, capture_output=True, text=True)

        # If the command fails, log the error
        if result.returncode != 0:
            print(f"Error processing {name}: {result.stderr}")
    except Exception as e:
        print(f"Failed to run command for {name}: {e}")

    with lock:
        pbar.update()  # Ensure pbar.update() is always inside the lock


# Read CSV and get package names
df = pd.read_csv(input_file)
files = df['Name'].to_list()
# get all package names has len over than 1
files = [name for name in files if len(name) > 1]


# Create progress bar
pbar = tqdm(total=len(files), desc="Processing", unit="name")

# Run tasks in parallel
with ThreadPoolExecutor() as executor:
    executor.map(run_odb, files)

# Close the progress bar
pbar.close()
