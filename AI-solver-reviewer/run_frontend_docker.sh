#!/bin/bash
# Docker Frontend Setup Script
# This script sets up and runs the frontend using Docker

echo "Setting up Frontend with Docker"
echo "==============================="
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Docker is not running. Please start Docker Desktop."
    exit 1
fi

echo "Docker is running!"
echo ""

# Navigate to frontend directory
cd "$(dirname "$0")/frontend"

echo "Building frontend Docker image..."
docker build -t ai-reviewer-frontend .

if [ $? -eq 0 ]; then
    echo "Frontend image built successfully!"
    echo ""
    echo "Starting frontend container..."
    echo "Frontend will be available at: http://localhost:3000"
    echo ""
    echo "Press Ctrl+C to stop the container"
    echo ""
    
    # Run the container
    docker run -it --rm \
        -p 3000:3000 \
        -v "$(pwd):/app" \
        -v "/app/node_modules" \
        -e REACT_APP_API_URL=http://localhost:8000 \
        ai-reviewer-frontend
else
    echo "Failed to build Docker image."
    exit 1
fi




