import subprocess

# Đường dẫn đến thư mục chứa lệnh oss-download
oss_download_path = r"..\..\tools\OSSGadget-0.1.422\src\oss-download\bin\Debug\net8.0"
download_directory = r"packages_possible_malware"
package_name = "lara"
package_version = "0.1.0"
command = f"oss-download.exe --extract --download-directory {download_directory} -c pkg:cargo/{package_name}@{package_version}"

subprocess.run(command, cwd=oss_download_path, shell=True)