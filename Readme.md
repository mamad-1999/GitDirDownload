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

## How to use

1. Run the script.
2. You will be prompted to enter the following information:
   - Repository Url: The Url of the repository.
   - GitHub access token: Your personal access token for authentication.
   - Number of download threads: How many concurrent downloads to perform (default is 20).
3. The tool will then download the specified file or directory and its contents.

## Features

- Downloads files concurrently for faster performance.
- Maintains the original directory structure.
- Logs each downloaded file in the terminal.
- Creates a main folder named after the last directory in the specified path.

## Notes

- Ensure you have a stable internet connection.
- The download speed depends on your internet connection and the number of threads used.
- Be aware of GitHub's API rate limits. This Script is efficient for repositories up to 100,000 files in the requested directory and its subdirectories.
- Keep your access token secure and never share it publicly.

## Requirements

- Python 3.6 or higher
- Required Python packages: requests

To install the required package, run:

`pip install -r requirements.txt`

## Installation

1. Clone this repository:

`git clone https://github.com/yourusername/github-directory-downloader.git`

2. Navigate to the project directory:

`cd github-directory-downloader`

3. Install the required packages:

`pip install -r requirements.txt`

## Running the Script

Run the script using Python:

`python github_directory_downloader.py`

For any issues or questions, please open an issue in this repository.

Now, here's the content for your requirements.txt file:

`requests==2.26.0`
