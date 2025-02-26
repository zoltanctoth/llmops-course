#!/usr/bin/env bash

# Get script directory path
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
PROJECT_DIR="$(readlink -f "${SCRIPT_DIR}/../")"

# Create MLflow data directory and ensure proper permissions
mkdir -p "${PROJECT_DIR}/.mlflow_data"
chmod -R 777 "${PROJECT_DIR}/.mlflow_data"

# Check if all required environment variables are set
required_vars=("MLFLOW_BACKEND_STORE_URI" "MLFLOW_DEFAULT_ARTIFACT_ROOT" "MLFLOW_HOST" "MLFLOW_PORT")
missing_vars=()

for var in "${required_vars[@]}"; do
  if [ -z "${!var}" ]; then
    missing_vars+=("$var")
  fi
done

# If any variables are missing, print error and exit
if [ ${#missing_vars[@]} -gt 0 ]; then
  echo "❌ Error: The following required environment variables are not set:"
  for var in "${missing_vars[@]}"; do
    echo "   - $var"
  done
  echo "Please set these variables in your environment or in .devcontainer/devcontainer.json"
  exit 1
fi

# Print startup message
echo "Starting MLflow server with configuration:"
echo "Backend Store URI: ${MLFLOW_BACKEND_STORE_URI}"
echo "Default Artifact Root: ${MLFLOW_DEFAULT_ARTIFACT_ROOT}"
echo "Host: ${MLFLOW_HOST}"
echo "Port: ${MLFLOW_PORT}"
echo -e "\033[1;32m🚀 Once MLflow is running, open a browser to \033[1;36mhttp://localhost:${MLFLOW_PORT}\033[1;32m by clicking the popup window! 🌐\033[0m"

# Start MLflow server without explicit parameters - relying on environment variables
mlflow server -w 1
