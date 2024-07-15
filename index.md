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


