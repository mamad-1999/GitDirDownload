import os
import requests
import concurrent.futures
from urllib.parse import urlparse, urljoin

def download_file(session, url, local_filename):
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

def download_github_content(url, token, threads=20):
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.strip('/').split('/')
    
    if len(path_parts) < 5:
        print("Invalid GitHub URL. Please provide a valid URL.")
        return
    
    owner = path_parts[0]
    repo = path_parts[1]
    branch = path_parts[3]
    path = '/'.join(path_parts[4:])
    
    api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': f'token {token}'
    }
    
    session = requests.Session()
    response = session.get(api_url, headers=headers)
    response.raise_for_status()
    tree = response.json()['tree']

    files_to_download = [item for item in tree if item['type'] == 'blob' and item['path'].startswith(path)]

    if not files_to_download:
        print(f"No files found in the specified path: {path}")
        return

    base_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/"

    if len(files_to_download) == 1 and files_to_download[0]['path'] == path:
        # It's a single file
        file = files_to_download[0]
        file_url = urljoin(base_url, file['path'])
        local_filename = os.path.basename(file['path'])
        download_file(session, file_url, local_filename)
        print(f"File '{local_filename}' downloaded.")
    else:
        # It's a directory
        main_dir = os.path.join('/downloads', os.path.basename(path.rstrip('/')))
        os.makedirs(main_dir, exist_ok=True)
        os.chmod('/downloads', 0o755)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            for file in files_to_download:
                file_url = urljoin(base_url, file['path'])
                local_path = os.path.join(main_dir, os.path.relpath(file['path'], path))
                futures.append(executor.submit(download_file, session, file_url, local_path))
            
            for future in concurrent.futures.as_completed(futures):
                future.result()

        print(f"All files downloaded to '{main_dir}' directory.")

def print_banner():
    banner = """
  ____ _ _   ____  _      ____                      _                 _ 
 / ___(_) |_|  _ \(_)_ __|  _ \  _____      ___ __ | | ___   __ _  __| |
| |  _| | __| | | | | '__| | | |/ _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |
| |_| | | |_| |_| | | |  | |_| | (_) \ V  V /| | | | | (_) | (_| | (_| |
 \____|_|\__|____/|_|_|  |____/ \___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|
                                                                        
    """
    blue = "\033[94m"
    reset = "\033[0m"
    print(f"{blue}{banner}{reset}")

def main():
    while True:
        print_banner()
        print("GitHub Content Downloader")
        print("===========================")
        print("1. Download GitHub content")
        print("2. Exit")
        
        choice = input("Enter your choice (1 or 2): ").strip()
        
        if choice == '2':
            print("Thank you for using GitDirDownload. Goodbye!")
            break
        elif choice == '1':
            url = input('Enter the GitHub URL of the file or directory to download: ')
            token = input('Enter your GitHub access token: ')
            threads = input('Enter the number of download threads (default is 20): ') or '20'

            try:
                threads = int(threads)
                if threads < 1:
                    raise ValueError
            except ValueError:
                print("Invalid thread count. Using default (20).")
                threads = 20

            print("\nStarting download...")
            download_github_content(url, token, threads)
            print("\nDownload completed!")
            
            input("\nPress Enter to continue...")
        else:
            print("Invalid choice. Please enter 1 or 2.")
        
        print("\n" + "="*30 + "\n")

if __name__ == '__main__':
    main()