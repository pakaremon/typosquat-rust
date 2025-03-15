import os
import zipfile

def unzip_all_files(directory):
    for filename in os.listdir(directory):
        print(f"Processing: {filename}")
        file_path = os.path.join(directory, filename)
        try:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(directory)
            print(f"Unzipped: {filename}")
        except zipfile.BadZipFile:
            print(f"Error: {filename} is not a valid zip file.")
        except Exception as e:
            print(f"Error: An unexpected error occurred while processing {filename}: {e}")

if __name__ == "__main__":
    directory = r"..\packages\get-package\packages"
    unzip_all_files(directory)