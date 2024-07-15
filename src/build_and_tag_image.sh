#!/bin/bash

# Set your variables in a local .env and source
source .env

# Build the Docker image
docker build -t gcr.io/$PROJECT_NUMBER/rss-updated .

# Optionally push the Docker image to Google Container Registry
docker push gcr.io/$PROJECT_NUMBER/rss-updated
