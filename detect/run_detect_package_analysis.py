import os
import subprocess
import pandas as pd
from tqdm import tqdm
from threading import Lock
import requests

# Thread-safe global variables
lock = Lock()
processing_names = set()

# Input and output paths
input_file = r"D:\HocTap\projectDrVuDucLy\Typosquatting_attacks_on_the_Rust_ecosystem\packages\detect\typosquatting_package_name.csv"
package_analysis_path = r"wsl /mnt/d/HocTap/projectDrVuDucLy/Typosquatting_attacks_on_the_Rust_ecosystem/packages/detect/run_analysis.sh"

output_dir = r"/mnt/d/HocTap/projectDrVuDucLy/Typosquatting_attacks_on_the_Rust_ecosystem/packages/detect/results/package_analysis"

window_output_dir = r"D:\HocTap\projectDrVuDucLy\Typosquatting_attacks_on_the_Rust_ecosystem\packages\detect\results\package_analysis"

def get_latest_crate_version(package_name):
    url = f"https://crates.io/api/v1/crates/{package_name}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data["crate"]["max_version"]
    else: 
        print(f"Error: Unable to fetch package info (Status Code: {response.status_code})")
        return None


def run_odb(name):
    """Runs oss-detect-backdoor for a given package name."""
    print("Processing " + name)

    with lock:
        if name in processing_names or  os.path.exists(os.path.join(window_output_dir, name + ".json")):
            pbar.update()  # Safely update progress bar
            print(f"File {name} already exists. Skipping.")
            return
        processing_names.add(name)

    # Build command using list format (safer than shell=True)
    command = [package_analysis_path, "-ecosystem crates.io", "-package", name, '-mode dynamic']

    try:
        result = subprocess.run(' '.join(command), capture_output=True, text=True)
        print(result.stdout)  # Print the standard output
        print(result.stderr)  # Print the standard error

        # If the command fails, log the error
        if result.returncode != 0:
            print(f"Error processing {name}: {result.stderr}")
            print(' '.join(command))
        
    except Exception as e:
        print(f"Failed to run command for {name}: {e}")
    finally:
        command = "wsl mv /tmp/results/" + name + ".json"  + " " + output_dir + "/" + name  + ".json"
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error copying {name}: {result.stderr}")
            print(' '.join(command))

    with lock:
        pbar.update()  # Ensure pbar.update() is always inside the lock


# Read CSV and get package names
df = pd.read_csv(input_file)
files = df['Package Name'].to_list()
# get all package names has len over than 1
files = [name for name in files if len(name) > 1]
print(f"Found {len(files)} package names.")

# Create progress bar
pbar = tqdm(total=len(files), desc="Processing", unit="name")

# Run tasks sequentially
for file in files:
    run_odb(file)

# Close the progress bar
pbar.close()
