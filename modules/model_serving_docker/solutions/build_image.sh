#!/bin/bash

set -e

echo "🏗️ Building Docker image..."
# Build the Docker image with build arguments

docker build -t model-serving .

echo "🎉 Docker image built successfully!"
