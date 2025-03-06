#!/bin/bash

# Source environment variables from workspace .env file
source "${WORKSPACE_FOLDER}/.env"

# Assert required environment variables are set
if [ -z "$AZURE_MLFLOW_TRACKING_URI" ]; then
    echo "Error: AZURE_MLFLOW_TRACKING_URI is not set"
    exit 1
fi

if [ -z "$GEMINI_API_KEY" ]; then
    echo "Error: GEMINI_API_KEY is not set"
    exit 1
fi

# Build the Docker image with build argument
docker build --build-arg AZURE_MLFLOW_TRACKING_URI="$AZURE_MLFLOW_TRACKING_URI" -t model-serving .

# Run the container with environment variables from current environment
docker run -p 8050:8000 \
  -e GEMINI_API_KEY="$GEMINI_API_KEY" \
  model-serving
