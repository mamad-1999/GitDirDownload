#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for required tools
docker_available=false
python_available=false

if command_exists docker; then
    docker_available=true
    echo "Docker is available."
else
    echo "Docker is not installed."
fi

if command_exists python3 && command_exists pip3; then
    python_available=true
    echo "Python3 and pip3 are available."
else
    echo "Python3 and/or pip3 are not installed."
fi

# Check if downloads folder exists, if not create it
if [ ! -d "downloads" ]; then
    echo "Creating downloads folder..."
    mkdir downloads
    echo "Downloads folder created."
else
    echo "Downloads folder already exists."
fi

# Set correct permissions for the downloads folder
echo "Setting correct permissions for downloads folder..."
chmod 755 downloads

# Ask user for preferred method
if $docker_available && $python_available; then
    echo "Both Docker and Python are available. Which method would you like to use?"
    echo "1) Docker"
    echo "2) Local Python"
    read -p "Enter your choice (1 or 2): " choice

    case $choice in
        1)
            use_docker=true
            ;;
        2)
            use_docker=false
            ;;
        *)
            echo "Invalid choice. Defaulting to Docker."
            use_docker=true
            ;;
    esac
elif $docker_available; then
    use_docker=true
elif $python_available; then
    use_docker=false
else
    echo "Neither Docker nor Python with pip are available. Please install one of them and try again."
    exit 1
fi

# Setup based on chosen method
if $use_docker; then
    echo "Setting up Docker environment..."
    
    # Build Docker image
    echo "Building Docker image..."
    docker build -t gitdirdownload .
    
    echo "Docker setup complete!"
    echo "To run the application with Docker, use the following command:"
    echo "docker run -it --rm -v \"\$(pwd)/downloads:/app/downloads\" gitdirdownload"
else
    echo "Setting up for local Python execution..."
    
    # Install required Python packages
    echo "Installing required Python packages..."
    pip3 install -r requirements.txt
    
    echo "Local Python setup complete!"
    echo "To run the application locally, use the following command:"
    echo "python3 github-download.py"
fi

echo "Setup complete!"