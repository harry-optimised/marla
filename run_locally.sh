#!/bin/bash

# Stop and remove any running containers with the same name
docker stop marla || true && docker rm marla || true

# Build the Docker image
docker build -t harryoptimised/marla:latest .

# Run the Docker container
docker run --name marla -p 8000:8000 harryoptimised/marla:latest