# GitHub Content Downloader

[![Python Version](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-blue)](https://www.python.org/downloads/)
[![GitHub Issues](https://img.shields.io/github/issues/mamad-1999/GitDirDownload)](https://github.com/mamad-1999/github-follow-insights/issues)
[![GitHub Stars](https://img.shields.io/github/stars/mamad-1999/GitDirDownload)](https://github.com/mamad-1999/github-follow-insights/stargazers)
[![GitHub License](https://img.shields.io/github/license/mamad-1999/GitDirDownload)](https://github.com/mamad-1999/github-follow-insights/blob/master/LICENSE)


<p>
    <a href="https://skillicons.dev">
      <img src="https://github.com/tandpfun/skill-icons/blob/main/icons/Python-Dark.svg" width="48" title="python">
      <img src="https://github.com/tandpfun/skill-icons/blob/main/icons/Github-Dark.svg" width="48" title="github">
    </a>
</p>

This tool allows you to download a specific file or directory and its contents from a GitHub repository.

![2024-07-19_15-32](https://github.com/user-attachments/assets/56eebbde-d3ae-4a91-a2a9-c96414919b8c)

## Features

- Downloads files concurrently for faster performance.
- Maintains the original directory structure.
- Logs each downloaded file in the terminal.

## Notes

- Ensure you have a stable internet connection.
- The download speed depends on your internet connection and the number of threads used.
- Be aware of GitHub's API rate limits. This Script is efficient for repositories up to 100,000 files in the requested directory and its subdirectories.
- Keep your access token secure and never share it publicly.

## Requirements

- Python 3.6 or higher
- Required Python packages: requests

## Installation

1. Clone this repository:

`git clone https://github.com/mamad-1999/GitDirDownload.git`

2. Run the install script:

```
chmod +x install.sh

./install.sh
```

This script will:
- Check for Docker and Python availability
- Create a 'downloads' folder if it doesn't exist
- Set correct permissions for the 'downloads' folder
- Ask you to choose between Docker and local Python setup (if both are available)
- Set up the environment based on your choice or availability

## Usage

After installation, run the application using the method you chose during setup:

### With Docker:
`docker run -it --rm -v "$(pwd)/downloads:/app/downloads" gitdirdownload`

### With local Python:
`python3 github-download.py`

Follow the prompts to download GitHub content. Downloaded files will be saved in the 'downloads' folder.
You will be prompted to enter the following information:
   - Repository Url: The Url of the repository.
   - GitHub access token: Your personal access token for authentication.
   - Number of download threads: How many concurrent downloads to perform (default is 20).
