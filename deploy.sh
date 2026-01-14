#!/bin/bash

# Deployment script for smart manufacturing application
set -e

echo "🚀 Starting deployment..."

# Configuration
CONTAINER_NAME="smart-manufacturing"
IMAGE_NAME="smart-manufacturing:latest"
PORT=5000

# Stop existing container
echo "🛑 Stopping existing container..."
docker stop $CONTAINER_NAME 2>/dev/null || true
docker rm $CONTAINER_NAME 2>/dev/null || true

# Build new image
echo "🔨 Building new image..."
docker build -t $IMAGE_NAME .

# Run new container
echo "🏃 Starting new container..."
docker run -d \
  --name $CONTAINER_NAME \
  -p $PORT:5000 \
  --restart unless-stopped \
  -v $(pwd)/artifacts:/app/artifacts:ro \
  -v $(pwd)/logs:/app/logs \
  $IMAGE_NAME

# Wait for container to be ready
echo "⏳ Waiting for application to be ready..."
sleep 10

# Health check
echo "🏥 Performing health check..."
if curl -f http://localhost:$PORT/health > /dev/null 2>&1; then
  echo "✅ Application is healthy and ready!"
  echo "🌐 Application available at: http://localhost:$PORT"
else
  echo "❌ Health check failed!"
  echo "📋 Container logs:"
  docker logs $CONTAINER_NAME
  exit 1
fi

echo "🎉 Deployment completed successfully!"