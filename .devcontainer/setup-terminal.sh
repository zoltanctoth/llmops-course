#!/usr/bin/env bash
set -e

# Ensure WORKSPACE_FOLDER is set
if [ -z "$WORKSPACE_FOLDER" ]; then
    export WORKSPACE_FOLDER="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
    echo "WORKSPACE_FOLDER was not set, using: $WORKSPACE_FOLDER"
fi

# Check if MLflow is running
if pgrep -f "mlflow server" > /dev/null; then
    echo "✅ MLflow server is already running"
else
    echo "⚠️ MLflow server is not running, starting it now..."
    
    # Ensure the MLflow script exists and is executable
    MLFLOW_SCRIPT="${WORKSPACE_FOLDER}/.devcontainer/start_mlflow.sh"
    if [ ! -f "$MLFLOW_SCRIPT" ]; then
        echo "ERROR: MLflow script not found at $MLFLOW_SCRIPT"
        exit 1
    fi

    if [ ! -x "$MLFLOW_SCRIPT" ]; then
        echo "Making MLflow script executable"
        chmod +x "$MLFLOW_SCRIPT"
    fi

    # Create log directory if it doesn't exist
    LOG_FILE="${WORKSPACE_FOLDER}/.mlflow.log"
    touch "$LOG_FILE"
    chmod 666 "$LOG_FILE"

    # Start MLflow in the background
    cd "${WORKSPACE_FOLDER}" && nohup bash -c "${MLFLOW_SCRIPT}" > "${LOG_FILE}" 2>&1 &

    # Store the PID of the MLflow process
    MLFLOW_PID=$!
    echo "MLflow started with PID: $MLFLOW_PID"

    # Wait a moment to see if the process stays alive
    sleep 2
    if ps -p $MLFLOW_PID > /dev/null; then
        echo "✅ MLflow server started successfully. Check logs at ${LOG_FILE}"
    else
        echo "❌ ERROR: MLflow server failed to start. Check logs at ${LOG_FILE}"
        cat "${LOG_FILE}"
    fi
fi

# Print MLflow access information
echo -e "📝 MLflow logs are at: ${WORKSPACE_FOLDER}/.mlflow.log\n"

