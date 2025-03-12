import os
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class GitHubFetcher:
    """
    Fetches test files from a public GitHub repository.
    """

    def __init__(self, owner, repo, branch="master", output_dir="downloaded_tests"):
        self.owner = owner
        self.repo = repo
        self.branch = branch
        self.output_dir = output_dir
        self.base_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
        
        # Define allowed file extensions (BDD + automation tests)
        self.allowed_extensions = [".feature", ".java", ".py", ".js", ".ts"]

        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

    def fetch_repo_files(self, path=""):
        """
        Recursively fetches test files from the GitHub repository.
        """
        url = f"{self.base_url}/{path}"
        logging.info(f"Fetching: {url}")

        response = requests.get(url)
        
        if response.status_code == 200:
            items = response.json()
            for item in items:
                if item["type"] == "file" and any(item["name"].endswith(ext) for ext in self.allowed_extensions):
                    self.download_file(item["download_url"], item["name"])
                elif item["type"] == "dir":
                    self.fetch_repo_files(item["path"])  # Recursively fetch directories
        else:
            logging.error(f"❌ Failed to fetch files: {response.status_code} - {response.text}")

    def download_file(self, url, filename):
        """
        Downloads a file and saves it locally.
        """
        response = requests.get(url)
        if response.status_code == 200:
            file_path = os.path.join(self.output_dir, filename)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(response.text)
            logging.info(f"✅ Downloaded: {filename}")
        else:
            logging.error(f"❌ Failed to download {filename}: {response.status_code}")

if __name__ == "__main__":
    # Replace with your repo details
    GITHUB_OWNER = "executeautomation"  
    GITHUB_REPO = "cucumberbasic"  

    fetcher = GitHubFetcher(GITHUB_OWNER, GITHUB_REPO)
    fetcher.fetch_repo_files()
    logging.info("✅ All test files downloaded!")
