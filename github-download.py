import os
import requests
import concurrent.futures
from urllib.parse import urlparse, urljoin
from abc import ABC, abstractmethod


class FileDownloader(ABC):
    @abstractmethod
    def download(self, session, url, local_filename):
        pass


class SimpleFileDownloader(FileDownloader):
    def download(self, session, url, local_filename):
        directory = os.path.dirname(local_filename)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with session.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"Downloaded: {local_filename}")
        return local_filename


class GitHubContentDownloader:
    def __init__(self, url, token, threads=20, downloader=SimpleFileDownloader()):
        self.url = url
        self.token = token
        self.threads = threads
        self.downloader = downloader
        self.session = requests.Session()
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
            'Authorization': f'token {token}'
        }

    def parse_github_url(self):
        parsed_url = urlparse(self.url)
        path_parts = parsed_url.path.strip('/').split('/')

        if len(path_parts) < 5:
            raise ValueError("Invalid GitHub URL. Please provide a valid URL.")

        return {
            'owner': path_parts[0],
            'repo': path_parts[1],
            'branch': path_parts[3],
            'path': '/'.join(path_parts[4:])
        }

    def get_github_tree(self, owner, repo, branch):
        api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
        response = self.session.get(api_url, headers=self.headers)
        response.raise_for_status()
        return response.json()['tree']

    def download_single_file(self, file_url, local_filename):
        return self.downloader.download(self.session, file_url, local_filename)

    def download_directory(self, base_url, files_to_download, main_dir, path):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = []
            for file in files_to_download:
                file_url = urljoin(base_url, file['path'])
                local_path = os.path.join(
                    main_dir, os.path.relpath(file['path'], path))
                futures.append(executor.submit(
                    self.download_single_file, file_url, local_path))

            for future in concurrent.futures.as_completed(futures):
                future.result()

    def download(self):
        try:
            url_parts = self.parse_github_url()
            tree = self.get_github_tree(
                url_parts['owner'], url_parts['repo'], url_parts['branch'])

            files_to_download = [item for item in tree if item['type']
                                 == 'blob' and item['path'].startswith(url_parts['path'])]

            if not files_to_download:
                print(
                    f"No files found in the specified path: {url_parts['path']}")
                return

            base_url = f"https://raw.githubusercontent.com/{url_parts['owner']}/{url_parts['repo']}/{url_parts['branch']}/"

            if len(files_to_download) == 1 and files_to_download[0]['path'] == url_parts['path']:
                # Single file download
                file = files_to_download[0]
                file_url = urljoin(base_url, file['path'])
                local_filename = os.path.basename(file['path'])
                self.download_single_file(file_url, local_filename)
                print(f"File '{local_filename}' downloaded.")
            else:
                # Directory download
                downloads_dir = os.path.join(os.getcwd(), 'downloads')
                main_dir = os.path.join(downloads_dir, os.path.basename(
                    url_parts['path'].rstrip('/')))
                os.makedirs(main_dir, exist_ok=True)
                self.download_directory(
                    base_url, files_to_download, main_dir, url_parts['path'])
                print(f"All files downloaded to '{main_dir}' directory.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")


class UserInterface:
    @staticmethod
    def print_banner():
        banner = """
      ____ _ _   ____  _      ____                      _                 _ 
     / ___(_) |_|  _ \(_)_ __|  _ \  _____      ___ __ | | ___   __ _  __| |
    | |  _| | __| | | | | '__| | | |/ _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |
    | |_| | | |_| |_| | | |  | |_| | (_) \ V  V /| | | | | (_) | (_| | (_| |
     \____|_|\__|____/|_|_|  |____/ \___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|
                                                                            
        """
        yellow = "\033[93m"
        reset = "\033[0m"
        print(f"{yellow}{banner}{reset}")

    @staticmethod
    def get_user_input():
        url = input(
            'Enter the GitHub URL of the file or directory to download: ')
        token = input('Enter your GitHub access token: ')
        threads = input(
            'Enter the number of download threads (default is 20): ') or '20'

        try:
            threads = int(threads)
            if threads < 1:
                raise ValueError
        except ValueError:
            print("Invalid thread count. Using default (20).")
            threads = 20

        return url, token, threads

    @staticmethod
    def run():
        while True:
            UserInterface.print_banner()
            print("GitHub Content Downloader")
            print("===========================")
            print("1. Download GitHub content")
            print("2. Exit")

            choice = input("Enter your choice (1 or 2): ").strip()

            if choice == '2':
                print("Thank you for using GitDirDownload. Goodbye!")
                break
            elif choice == '1':
                url, token, threads = UserInterface.get_user_input()
                downloader = GitHubContentDownloader(url, token, threads)
                print("\nStarting download...")
                downloader.download()
                print("\nDownload completed!")

                input("\nPress Enter to continue...")
            else:
                print("Invalid choice. Please enter 1 or 2.")

            print("\n" + "="*30 + "\n")


if __name__ == '__main__':
    UserInterface.run()
