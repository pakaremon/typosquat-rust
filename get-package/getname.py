import requests

API_KEY = "17831f748780939c00b6150f7e1259aa"
BASE_URL = "https://libraries.io/api/search?platforms=Cargo&sort=dependent_repos_count&per_page=100"

top_packages = []
datas = []  

for page in range(1, 3):  # Get page 1 and page 2 (200 results total)
    url = f"{BASE_URL}&page={page}&api_key={API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if not data:
            break  # Stop if no more results
        datas.append(data)
        top_packages.extend([pkg["name"] for pkg in data])
        print(f"Fetched {len(data)} packages from page {page}")
    else:
        print(f"Error: {response.status_code} - {response.text}")
        break

print(f"Total top packages fetched: {len(top_packages)}")
print(top_packages)

# Save the top packages to a file
with open("top_packages.txt", "w") as file:
    for pkg in top_packages:
        file.write(pkg + "\n")