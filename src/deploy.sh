#!/bin/bash

# Function to display usage
usage() {
    echo "Usage: $0 --dev | --prod [--update-secrets]"
    exit 1
}

# Check if the correct number of arguments is provided
if [ $# -lt 1 ] || [ $# -gt 2 ]; then
    usage
fi

# Initialize variables
UPDATE_SECRETS=false

# Determine the environment and other configurations based on the argument
for arg in "$@"
do
    case "$arg" in
        --dev)
            IMAGE_TAG="dev"
            ;;
        --prod)
            IMAGE_TAG="latest"
            ;;
        --update-secrets)
            UPDATE_SECRETS=true
            ;;
        *)
            usage
            ;;
    esac
done

# Source environment variables from .env file
source .env

# Prepare the gcloud run deploy command
DEPLOY_COMMAND="gcloud run deploy rss-updater \
    --image us-west2-docker.pkg.dev/$PROJECT_NAME/rss-updater/rss-updater-image:$IMAGE_TAG \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated"

# Add update secrets arguments if --update-secrets is specified
if [ "$UPDATE_SECRETS" = true ]; then
    DEPLOY_COMMAND="$DEPLOY_COMMAND \
        --update-secrets INSTANCE_CONNECTION_NAME=INSTANCE_CONNECTION_NAME:latest \
        --update-secrets DB_USER=DB_USER:latest \
        --update-secrets DB_PASS=DB_PASS:latest \
        --update-secrets DB_NAME=DB_NAME:latest"
fi

# Execute the deploy command
eval $DEPLOY_COMMAND

# Check if the gcloud command succeeded
if [ $? -eq 0 ]; then
    echo "Deployment to ${IMAGE_TAG} environment successful."
else
    echo "Deployment to ${IMAGE_TAG} environment failed."
fi
