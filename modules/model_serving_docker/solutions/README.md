# Docker Model Serving

This directory contains scripts for building, running, and testing a Docker container that serves an ML model using FastAPI.

## Files

- `Dockerfile`: Defines the Docker image for the model serving container
- `build_image.sh`: Script to build the Docker image
- `run_container.sh`: Script to run the Docker container
- `test_service.sh`: Script to test the model serving API
- `model_serving.py`: FastAPI application for serving the model
- `requirements.txt`: Python dependencies for the FastAPI application
- `model/`: Directory containing the MLflow model

## Docker-in-Docker Networking

When running Docker inside a devcontainer (Docker-in-Docker), there are some networking considerations to be aware of:

### Issue: Accessing container ports in Docker-in-Docker environments

In a Docker-in-Docker environment, accessing container ports can be challenging. Depending on the specific environment configuration, you might need to use different approaches:

1. **Standard port mapping**: Using `-p 8421:8421` to map the container port to the host
2. **Container IP address**: Accessing the container directly via its IP address

### Solution: Flexible connection approach

To handle these networking challenges, the scripts in this directory have been updated to:

1. Run the container in detached mode with a specific name and standard port mapping
2. Try connecting via localhost first (which works in many environments)
3. If localhost fails, fall back to using the container's IP address
4. Provide clear feedback about which connection method worked

## Usage

1. Build the Docker image:
   ```bash
   ./build_image.sh
   ```

2. Run the Docker container:
   ```bash
   ./run_container.sh
   ```
   This will display the container's IP address and example commands for accessing the API.

3. Test the API:
   ```bash
   ./test_service.sh
   ```
   This will test both the health check endpoint and the summarization endpoint.

## Manual Testing

You can test the API manually using curl with either localhost or the container's IP address:

```bash
# Option 1: Using localhost (if it works in your environment)
# Health check
curl http://localhost:8421/health

# Summarize text
curl -X POST http://localhost:8421/summarize \
  -H "Content-Type: application/json" \
  -d '{"text": "LLMOps is on the rise!"}'

# Option 2: Using container IP (if localhost doesn't work)
# Get the container's IP address
CONTAINER_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' model-serving-container)

# Health check
curl http://$CONTAINER_IP:8421/health

# Summarize text
curl -X POST http://$CONTAINER_IP:8421/summarize \
  -H "Content-Type: application/json" \
  -d '{"text": "LLMOps is on the rise!"}'
