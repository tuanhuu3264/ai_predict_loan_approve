#!/bin/bash

# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Python and pip
sudo apt-get install -y python3-pip python3-dev

# Install Docker
sudo apt-get install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install AWS CLI
sudo apt-get install -y awscli

# Create project directory
mkdir -p /home/ubuntu/loan_scoring
cd /home/ubuntu/loan_scoring

# Clone repository (replace with your repository URL)
git clone <your-repo-url> .

# Install Python dependencies
pip3 install -r requirements.txt

# Start the application using Docker Compose
docker-compose up -d 