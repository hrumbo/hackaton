import os
import requests

# GitHub Repository Info
GITHUB_OWNER = "executeautomation"  # Change this to the owner (e.g., "cucumber")
GITHUB_REPO = "cucumberbasic"  # Change this to the repository name (e.g., "cucumber-jvm")
GITHUB_BRANCH = "master"  # The branch to fetch from

# Folder to save test files
OUTPUT_DIR = "downloaded_tests"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# File extensions to filter (BDD + automation test types)
ALLOWED_EXTENSIONS = [".feature", ".java", ".py", ".js", ".ts"]

# GitHub API URL
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents"

def fetch_repo_files(path=""):
    """ Recursively fetch files from a GitHub repository """
    url = f"{GITHUB_API_URL}/{path}"
    response = requests.get(url)
    
    if response.status_code == 200:
        items = response.json()
        for item in items:
            if item["type"] == "file" and any(item["name"].endswith(ext) for ext in ALLOWED_EXTENSIONS):
                download_file(item["download_url"], item["name"])
            elif item["type"] == "dir":
                fetch_repo_files(item["path"])  # Recursively fetch directories
    else:
        print(f"Failed to fetch files: {response.status_code}, {response.text}")

def download_file(url, filename):
    """ Download a file and save it locally """
    response = requests.get(url)
    if response.status_code == 200:
        file_path = os.path.join(OUTPUT_DIR, filename)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(response.text)
        print(f"✅ Downloaded: {filename}")
    else:
        print(f"❌ Failed to download {filename}: {response.status_code}")

if __name__ == "__main__":
    print(f"🔍 Fetching test files from {GITHUB_OWNER}/{GITHUB_REPO}...")
    fetch_repo_files()
    print("✅ All test files downloaded!")
