
# Local Testing Guide for Flask Application in Docker

This guide provides step-by-step instructions on how to test your Flask application locally using Docker.

## Prerequisites

- Docker installed on your local machine
- Flask application with a Dockerfile
- `.env` file with environment variables
- `secret.json` file for Google Application Credentials

## Step 1: Prepare the `.env` File

Create a `.env` file in your project directory with the following content:

```env
GOOGLE_APPLICATION_CREDENTIALS=/app/secret.json
INSTANCE_CONNECTION_NAME=smart-axis-421517:us-west2:jnapolitano-site
DB_USER=cobra
DB_PASS=iwanttocreatesomethingnew5498
DB_NAME=jnapolitano
PORT=8080
```

## Step 2: Ensure `secret.json` is Included in the Docker Image

Your Dockerfile should include a line to copy the `secret.json` file into the `/app` directory in the Docker image. Here is an example Dockerfile:

```Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Ensure the secret.json file is copied into the container
COPY secret.json /app/secret.json

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run gunicorn when the container launches
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
```

## Step 3: Build the Docker Image

If you have made changes to the Dockerfile or added the `secret.json` file, build the Docker image:

```bash
docker build -t flask-app .
```

## Step 4: Run the Docker Container with the `.env` File

Use the `--env-file` option to pass the environment variables from your `.env` file to the Docker container:

```bash
docker run --env-file .env -p 8080:8080 flask-app
```

## Step 5: Verify Environment Variables Inside the Container

To verify that the environment variables are set correctly, start the container in interactive mode:

```bash
docker run -it --env-file .env flask-app /bin/sh
```

Once inside the container, check the environment variables:

```sh
echo $GOOGLE_APPLICATION_CREDENTIALS
echo $INSTANCE_CONNECTION_NAME
echo $DB_USER
echo $DB_PASS
echo $DB_NAME
echo $PORT
```

## Step 6: Test the Endpoints Locally

Create test scripts to test the endpoints.

### Create `test_update_builds_local.sh`

Create a file named `test_update_builds_local.sh` with the following content:

```bash
#!/bin/bash

curl -X POST \
  http://127.0.0.1:8080/update/builds \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "New Build Example",
    "link": "http://example.com/build",
    "description": "This is a description of the build process.",
    "generator": "Build Generator 1.0",
    "language": "Python",
    "copyright": "2024 Example Corp",
    "lastBuildDate": "2024-07-11T16:26:32",
    "atom_link_href": "http://example.com/index.xml",
    "atom_link_rel": "self",
    "atom_link_type": "application/rss+xml"
}'
```

### Create `test_update_feeds_local.sh`

Create a file named `test_update_feeds_local.sh` with the following content:

```bash
#!/bin/bash

curl -X POST \
  http://127.0.0.1:8080/update/feeds \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "Create and Deploy Cloud Run Job Script",
    "link": "http://jnapolitano.com/posts/create_deploy_cloud_run_job/",
    "pubDate": "2024-07-11T16:26:32",
    "guid": "http://jnapolitano.com/posts/create_deploy_cloud_run_job/",
    "description": "Cloud Run Job Deployment Script This repository contains a script to build and deploy a Python application as a Cloud Run Job using Google Cloud Build. The script dynamically generates a cloudbuild.yaml file and submits it to Google Cloud Build. Prerequisites Before using the deployment script, ensure you have the following: Google Cloud SDK: Installed and configured. Docker: Installed. Google Cloud Project: Created and configured. Service Account Key: A service account key JSON file with appropriate permissions stored at keys/service-account-key."
}'
```

### Make the Scripts Executable

Make the scripts executable:

```bash
chmod +x test_update_builds_local.sh
chmod +x test_update_feeds_local.sh
```

### Run the Scripts to Test the Endpoints Locally

Run the scripts:

```bash
./test_update_builds_local.sh
./test_update_feeds_local.sh
```

## Expected Response

You should receive a JSON response indicating the success or failure of the request. If successful, it will look like this:

### Expected Response for `test_update_builds_local.sh`

```json
{
  "message": "Build record added successfully"
}
```

### Expected Response for `test_update_feeds_local.sh`

```json
{
  "message": "Feed record added successfully"
}
```

## Troubleshooting

If you encounter any issues:

- **Check Docker Logs**: To view logs from the running container, use:
  ```bash
  docker logs <container_id>
  ```

- **Database Connectivity**: Ensure that your local environment can connect to the database. If you're using a local database, make sure the credentials and host are correct.

By following these steps, you can verify that your Docker container is working as expected locally before deploying it to Google Cloud Run.
