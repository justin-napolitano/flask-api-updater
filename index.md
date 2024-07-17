+++
title =  "Automate Posting Hugo Blog to Social Sites (with a db) Part 4"
date = "2024-07-12"
description = "Creating a CMS DB.. Because why not"
author = "Justin Napolitano"
tags = ['python', "hugo","programming","fail"]
images = ["images/feature-image.png"]
categories = ['Projects']
+++


# GCP Flask App

I created a db.. now I need update a few tables. Since the db is in gcp. I amgoing to create a quick flask app that will update the tables..

I am using the quick start to get this one going.

Source: ```https://github.com/justin-napolitano/python-docs-samples/tree/main/cloud-sql/mysql/sqlalchemy```


## Create a New Local Service Account

Create a new local service account to be able to test the app locally. 



## Create a new role for the cloud run service account

Reference : [Reference Material](https://cloud.google.com/sql/docs/mysql/connect-instance-cloud-run#deploy_sample_app_to)


Add the cloud run clien to the service account.. Follow directions above. 

## To run locally we need some environmental variables

There is a secrent manager available from google.. i will update all code to use that in the future. 

[secret manager documentation](https://cloud.google.com/secret-manager/docs/overview)


I created a .env with the following

GOOGLE_APPLICATION_CREDENTIALS='secret.json'
INSTANCE_CONNECTION_NAME='smart-axis-421517:us-west2:jnapolitano-site'
DB_USER='cobra'
DB_PASS='your pass'
DB_NAME='jnapolitano'


## Install Reqs

```bash
virtualenv --python python3 env
source env/bin/activate
pip install -r requirements.txt
```

### Test the Application

```bash
python app.py
```

Navigate towards http://127.0.0.1:8080 to verify your application is running correctly.


## Modify the app for our needs

So the base app is a simple app that creates a table called votes and records the information.. I want to add two routes that will update two seperate tables in my database. 

### Feed Route

```python

@app.route('/update/feed', methods=['POST'])
def update_feed():
    data = request.json
    title = data.get('title')
    link = data.get('link')
    pubDate = data.get('pubDate')
    guid = data.get('guid')
    description = data.get('description')

    stmt = sqlalchemy.text(
        "INSERT INTO feed (title, link, pubDate, guid, description) VALUES (:title, :link, :pubDate, :guid, :description)"
    )
    try:
        with db.connect() as conn:
            conn.execute(stmt, parameters={
                "title": title,
                "link": link,
                "pubDate": pubDate,
                "guid": guid,
                "description": description
            })
            conn.commit()
    except Exception as e:
        logger.exception(e)
        return jsonify({'message': 'Error updating feed table'}), 500

    return jsonify({'message': 'Feed record added successfully'}), 201


```

### Update Build Route


```python
@app.route('/update/builds', methods=['POST'])
def update_builds():
    data = request.json
    title = data.get('title')
    link = data.get('link')
    description = data.get('description')
    generator = data.get('generator')
    language = data.get('language')
    copyright = data.get('copyright')
    last_build_date = data.get('lastBuildDate')
    atom_link_href = data.get('atom_link_href')
    atom_link_rel = data.get('atom_link_rel')
    atom_link_type = data.get('atom_link_type')

    stmt = sqlalchemy.text(
        "INSERT INTO builds (title, link, description, generator, language, copyright, lastBuildDate, atom_link_href, atom_link_rel, atom_link_type) "
        "VALUES (:title, :link, :description, :generator, :language, :copyright, :lastBuildDate, :atom_link_href, :atom_link_rel, :atom_link_type)"
    )
    try:
        with db.connect() as conn:
            conn.execute(stmt, parameters={
                "title": title,
                "link": link,
                "description": description,
                "generator": generator,
                "language": language,
                "copyright": copyright,
                "lastBuildDate": last_build_date,
                "atom_link_href": atom_link_href,
                "atom_link_rel": atom_link_rel,
                "atom_link_type": atom_link_type
            })
            conn.commit()
    except Exception as e:
        logger.exception(e)
        return jsonify({'message': 'Error updating builds table'}), 500

    return jsonify({'message': 'Build record added successfully'}), 201
```

## Test it out

### Update-feed

create a bash called test-update-feed.sh... chmod +x it and then run.. You should get a response that says updated successfully. 

```bash

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

```

### Update build

Same as above but with this code

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

## Testing the Container Locally

Once the app is confirmed to work we should test that the container builds as expected. 


### Prerequisites

- Docker installed on your local machine
- Flask application with a Dockerfile
- `.env` file with environment variables
- `secret.json` file for Google Application Credentials

### Step 1: Prepare the `.env` File

Create a `.env` file in your project directory with the following content:

```env
GOOGLE_APPLICATION_CREDENTIALS=secret-path
INSTANCE_CONNECTION_NAME=your-instance
DB_USER=your=user
DB_PASS=yuour-pass
DB_NAME={your-db}
PORT=8080
```

### Step 2: Ensure `secret.json` is Included in the Docker Image

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

### Step 4: Run the Docker Container with the `.env` File

Use the `--env-file` option to pass the environment variables from your `.env` file to the Docker container:

```bash
docker run --env-file .env -p 8080:8080 flask-app
```

### Step 5: Verify Environment Variables Inside the Container

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

### Step 6: Test the Endpoints Locally

Create test scripts to test the endpoints.

#### Create `test_update_builds_local.sh`

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

#### Create `test_update_feeds_local.sh`

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

#### Make the Scripts Executable

Make the scripts executable:

```bash
chmod +x test_update_builds_local.sh
chmod +x test_update_feeds_local.sh
```

#### Run the Scripts to Test the Endpoints Locally

Run the scripts:

```bash
./test_update_builds_local.sh
./test_update_feeds_local.sh
```

### Expected Response

You should receive a JSON response indicating the success or failure of the request. If successful, it will look like this:

#### Expected Response for `test_update_builds_local.sh`

```json
{
  "message": "Build record added successfully"
}
```

#### Expected Response for `test_update_feeds_local.sh`

```json
{
  "message": "Feed record added successfully"
}
```

### Troubleshooting

If you encounter any issues:

- **Check Docker Logs**: To view logs from the running container, use:
  ```bash
  docker logs <container_id>
  ```

- **Database Connectivity**: Ensure that your local environment can connect to the database. If you're using a local database, make sure the credentials and host are correct.


## Building and Deploying the container to gcp



### Step 1: Create and Configure Environment Variables

1. **Create a `.env` File**

Create a `.env` file in your project directory with the following content:

```env
PROJECT_NAME=your-project-name
PROJECT_NUMBER=67904901121
REGION=us-west2
SERVICE_ACCOUNT=your-service-account
INSTANCE_CONNECTION_NAME=your-instance-connection-name
DB_USER=your-db-user
DB_PASS=your-db-password
DB_NAME=your-db-name
```

Replace the placeholder values (your-project-name, your-service-account, your-instance-connection-name, your-db-user, your-db-password, and your-db-name) with your actual values.

### Step 2: Manage Secrets

```bash
#!/bin/bash

# Set your variables in a local .env and source
source .env

# Enable the Secret Manager API
gcloud services enable secretmanager.googleapis.com

# Create secrets in Secret Manager
echo -n $INSTANCE_CONNECTION_NAME | \
    gcloud secrets create INSTANCE_CONNECTION_NAME --data-file=-

echo -n $DB_USER | \
    gcloud secrets create DB_USER --data-file=-

echo -n $DB_PASS | \
    gcloud secrets create DB_PASS --data-file=-

echo -n $DB_NAME | \
    gcloud secrets create DB_NAME --data-file=-

# Grant access to the Cloud Run service account
gcloud secrets add-iam-policy-binding INSTANCE_CONNECTION_NAME \
    --member=serviceAccount:$SERVICE_ACCOUNT \
    --role=roles/secretmanager.secretAccessor

gcloud secrets add-iam-policy-binding DB_USER \
    --member=serviceAccount:$SERVICE_ACCOUNT \
    --role=roles/secretmanager.secretAccessor

gcloud secrets add-iam-policy-binding DB_PASS \
    --member=serviceAccount:$SERVICE_ACCOUNT \
    --role=roles/secretmanager.secretAccessor

gcloud secrets add-iam-policy-binding DB_NAME \
    --member=serviceAccount:$SERVICE_ACCOUNT \
    --role=roles/secretmanager.secretAccessor
```

### Create the Artifact Repository

Create

```bash
#!/bin/bash

# Set your variables in a local .env and source
source .env

# Create the Artifact Registry repository
gcloud artifacts repositories create rss-updated \
    --repository-format=docker \
    --location=$REGION \
    --description="Docker repository for RSS Updater"

# Verify the repository creation
gcloud artifacts repositories list --location=$REGION

```

Make sure to chmod +x the script

### Build the Docker Image with Cloud Build

#### Create cloudbuild.yaml

```yaml

steps:
- name: 'gcr.io/cloud-builders/docker'
  args: [
    'build',
    '-t',
    'us-west2-docker.pkg.dev/${_PROJECT_NAME}/rss-updated/rss-updated-image:latest',
    '.'
  ]
images:
- 'us-west2-docker.pkg.dev/${_PROJECT_NAME}/rss-updated/rss-updated-image:latest'
substitutions:
  _PROJECT_NAME: "your-project-name"
```

#### Trigger the Build

```bash

#!/bin/bash

# Set your variables in a local .env and source
source .env

# Trigger the Cloud Build with custom substitution
gcloud builds submit --config=cloudbuild.yaml --substitutions=_PROJECT_NAME=$PROJECT_NAME

```

```bash
chmod +x trigger_cloud_build.sh
./trigger_cloud_build.sh
```

#### Deploy to Cloud Run

```bash

#!/bin/bash

# Set your variables in a local .env and source
source .env

# Deploy to Cloud Run
gcloud run deploy rss-updated \
    --image us-west2-docker.pkg.dev/$PROJECT_NAME/rss-updated/rss-updated-image:latest \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --update-secrets INSTANCE_CONNECTION_NAME=INSTANCE_CONNECTION_NAME:latest \
    --update-secrets DB_USER=DB_USER:latest \
    --update-secrets DB_PASS=DB_PASS:latest \
    --update-secrets DB_NAME=DB_NAME:latest
```

```bash

chmod +x deploy_to_cloud_run.sh
./deploy_to_cloud_run.sh
```


## Updating the Endpoint to account for Existing posts

### Updating the feed endpoint to account for existing 

```python

@app.route('/update/feed', methods=['POST'])
def update_feed():
    data = request.json
    title = data.get('title')
    link = data.get('link')
    pubDate = data.get('pubDate')
    guid = data.get('guid')
    description = data.get('description')

    stmt_select = sqlalchemy.text(
        "SELECT pubDate FROM feed WHERE guid = :guid"
    )
    stmt_insert = sqlalchemy.text(
        "INSERT INTO feed (title, link, pubDate, guid, description) VALUES (:title, :link, :pubDate, :guid, :description)"
    )
    stmt_update = sqlalchemy.text(
        "UPDATE feed SET title = :title, link = :link, pubDate = :pubDate, description = :description WHERE guid = :guid"
    )

    try:
        with db.connect() as conn:
            result = conn.execute(stmt_select, {"guid": guid}).fetchone()
            if result:
                existing_pubDate = result[0]
                if existing_pubDate != pubDate:
                    conn.execute(stmt_update, {
                        "title": title,
                        "link": link,
                        "pubDate": pubDate,
                        "guid": guid,
                        "description": description
                    })
                    conn.commit()
                    return jsonify({'message': 'Feed record updated successfully'}), 200
                else:
                    return jsonify({'message': 'No update needed for the feed record'}), 200
            else:
                conn.execute(stmt_insert, {
                    "title": title,
                    "link": link,
                    "pubDate": pubDate,
                    "guid": guid,
                    "description": description
                })
                conn.commit()
                return jsonify({'message': 'Feed record added successfully'}), 201
    except Exception as e:
        logger.exception(e)
        return jsonify({'message': 'Error updating feed table'}), 500
```

