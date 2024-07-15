#!/bin/bash

# Create a .env file in your project directory with the following content:
# PROJECT_NAME=your-project-name
# PROJECT_NUMBER=67904901121
# REGION=us-west2
# SERVICE_ACCOUNT=your-service-account
# INSTANCE_CONNECTION_NAME=your-instance-connection-name
# DB_USER=your-db-user
# DB_PASS=your-db-password
# DB_NAME=your-db-name

# Set your variables in a local .env and source
source .env

# Deploy to Cloud Run
gcloud run deploy rss-updater \
    --image us-west2-docker.pkg.dev/$PROJECT_NAME/rss-updater/rss-updater-image:latest \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --update-secrets INSTANCE_CONNECTION_NAME=INSTANCE_CONNECTION_NAME:latest \
    --update-secrets DB_USER=DB_USER:latest \
    --update-secrets DB_PASS=DB_PASS:latest \
    --update-secrets DB_NAME=DB_NAME:latest
