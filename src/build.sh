#!/bin/bash

# Function to display usage
usage() {
    echo "Usage: $0 --dev | --prod"
    exit 1
}

# Check if the correct number of arguments is provided
if [ $# -ne 1 ]; then
    usage
fi

# Determine the configuration file based on the argument
case "$1" in
    --dev)
        CONFIG_FILE="cloudbuild-dev.yaml"
        ;;
    --prod)
        CONFIG_FILE="cloudbuild-prod.yaml"
        ;;
    *)
        usage
        ;;
esac

# Execute the gcloud build submit command with the appropriate configuration file
gcloud builds submit --config="$CONFIG_FILE" .

# Check if the gcloud command succeeded
if [ $? -eq 0 ]; then
    echo "Deployment to ${1#--} environment successful."
else
    echo "Deployment to ${1#--} environment failed."
fi
