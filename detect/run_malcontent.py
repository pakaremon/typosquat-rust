import sys
import os
from os import listdir
from os.path import isfile, join
import subprocess
from pathlib import Path


mypath = sys.argv[1]
onlyfiles = [(f, join(mypath, f)) for f in listdir(mypath) if isfile(join(mypath, f))]


def run_linux_command(command, result_path):
    try:
        # Run the command and capture the output
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        # Check if the command was successful
        if result.returncode == 0:
            print("Command executed successfully!")
            print("Output:\n", result.stdout)
        else:
            print(f"Command failed with error code {result.returncode}")
            print("Error:\n", result.stderr)
            os.remove(result_path)

    except Exception as e:
        print(f"An error occurred: {e}")



for f, path in onlyfiles:
    print(f)
    filename_wo_ext = Path(path).with_suffix('').name
    result_path = os.path.join(sys.argv[2], filename_wo_ext + ".json")
    if not os.path.exists(result_path):
        command = 'mal --format=json --min-risk=high -o {} analyze {}'.format(result_path, path)
       
        run_linux_command(command, result_path)
