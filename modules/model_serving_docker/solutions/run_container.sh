# Run the container with environment variables from current environment
# Check if WORKSPACE_FOLDER is set and .env file exists
if [ ! -z "$WORKSPACE_FOLDER/.env" ]; then
    echo "📁 Using WORKSPACE_FOLDER for loading .env file: $WORKSPACE_FOLDER"
    . "$WORKSPACE_FOLDER/.env"
fi

# Assert required environment variables are set
if [ -z "$GEMINI_API_KEY" ]; then
    echo "❌ Error: GEMINI_API_KEY is not set"
    exit 1
fi

echo "🚀 Starting container, listening on port 8421..."
# Run in detached mode with standard port mapping
docker run -d \
  --name model-serving-container \
  -p 8421:8421 \
  -e GEMINI_API_KEY="$GEMINI_API_KEY" \
  model-serving

# Wait a moment for the container to start
sleep 2

# Check if the container is running
if docker ps | grep -q "model-serving-container"; then
  echo "✅ Container started successfully"
  echo "🌐 Access the API at: http://localhost:8421"
  echo "🔍 Health check: curl http://localhost:8421/health"
  echo "📝 Example request: curl -X POST http://localhost:8421/summarize -H \"Content-Type: application/json\" -d '{\"text\": \"LLMOps is on the rise!\"}'"

  echo "📋 Container logs:"
  docker logs model-serving-container
else
  echo "❌ Container failed to start"
  echo "📋 Container logs:"
  docker logs model-serving-container
fi
