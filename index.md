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

