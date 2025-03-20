#!/bin/bash

echo "🚀 Starting Docker service test..."

# Check if container is running
if ! docker ps | grep -q "model-serving-container"; then
    echo "📦 Container not running. Starting it..."
    # Remove any existing container with the same name
    docker rm -f model-serving-container 2>/dev/null || true
    # Start the container
    ./run_container.sh
    # Wait for container to start
    echo "⏳ Waiting for container to start..."
    sleep 5
else
    echo "📦 Container already running"
fi

# Check container status again
if ! docker ps | grep -q "model-serving-container"; then
    echo "❌ Container failed to start or stay running"
    echo "📋 Container logs:"
    docker logs model-serving-container
    exit 1
fi

# Test the summarization endpoint
echo "🔍 Testing summarization endpoint..."
echo "📝 Sending test request..."

# Get the container's IP address
CONTAINER_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' model-serving-container)
echo "🔌 Container IP: $CONTAINER_IP"

# Try both localhost and container IP
echo "🔍 Trying both localhost and container IP..."

# First try localhost
echo "🩺 Checking health endpoint via localhost..."
localhost_response=$(curl -s http://localhost:8421/health 2>/dev/null)
if [ $? -eq 0 ] && [ ! -z "$localhost_response" ]; then
  echo "✅ Successfully connected via localhost"
  USE_LOCALHOST=true
  health_response=$localhost_response
else
  echo "❌ Failed to connect via localhost"
  USE_LOCALHOST=false

  # Try container IP
  echo "🩺 Checking health endpoint via container IP..."
  container_ip_response=$(curl -s http://$CONTAINER_IP:8421/health 2>/dev/null)
  if [ $? -eq 0 ] && [ ! -z "$container_ip_response" ]; then
    echo "✅ Successfully connected via container IP"
    health_response=$container_ip_response
  else
    echo "❌ Failed to connect via container IP"
    echo "❌ Cannot connect to the container. Please check the container logs."
    docker logs model-serving-container
    exit 1
  fi
fi

echo "Health check response: $health_response"

# Now test the summarization endpoint
if [ "$USE_LOCALHOST" = true ]; then
  echo "📝 Using localhost for summarization request..."
  response=$(curl -sv -X POST http://localhost:8421/summarize \
    -H "Content-Type: application/json" \
    -d '{"text": "LLMOps is on the rise!"}')
else
  echo "📝 Using container IP for summarization request..."
  response=$(curl -sv -X POST http://$CONTAINER_IP:8421/summarize \
    -H "Content-Type: application/json" \
    -d '{"text": "LLMOps is on the rise!"}')
fi

# Check if the request was successful
if [ $? -eq 0 ]; then
    echo "✅ Request successful!"
    echo "📦 Response:"
    echo "$response" | jq '.'
else
    echo "❌ Request failed!"
    echo "$response"
    exit 1
fi

echo "✨ Test completed!"
