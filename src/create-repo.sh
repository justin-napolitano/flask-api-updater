
# Create the Artifact Registry repository
gcloud artifacts repositories create rss-updater \
    --repository-format=docker \
    --location=$REGION \
    --description="Docker repository for RSS Updater"

# Verify the repository creation
gcloud artifacts repositories list --location=$REGION
