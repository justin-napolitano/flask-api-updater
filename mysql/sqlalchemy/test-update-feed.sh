#!/bin/bash

curl -X POST \
  http://127.0.0.1:8080/update/feed \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "Create and Deploy Cloud Run Job Script",
    "link": "http://jnapolitano.com/posts/create_deploy_cloud_run_job/",
    "pubDate": "2024-07-11T16:26:32",
    "guid": "http://jnapolitano.com/posts/create_deploy_cloud_run_job/",
    "description": "Cloud Run Job Deployment Script This repository contains a script to build and deploy a Python application as a Cloud Run Job using Google Cloud Build. The script dynamically generates a cloudbuild.yaml file and submits it to Google Cloud Build. Prerequisites Before using the deployment script, ensure you have the following: Google Cloud SDK: Installed and configured. Docker: Installed. Google Cloud Project: Created and configured. Service Account Key: A service account key JSON file with appropriate permissions stored at keys/service-account-key."
}'
