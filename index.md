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



## Create a new role for the cloud run service account

Reference : [Reference Material](https://cloud.google.com/sql/docs/mysql/connect-instance-cloud-run#deploy_sample_app_to)

```bash 

gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/run-sql

`
### Write an initialization script


```bash
#!/bin/bash

# Source the .env file to load environment variables
set -o allexport
source .env
set -o allexport

# Set other variables
PROJECT_ID="smart-axis-421517"
INSTANCE_NAME="jnapolitano-db"
REGION="us-west2" # e.g., us-central1
DATABASE_NAME="jnapolitano"
BUILDS_SQL_FILE="builds.sql" # Name of your builds SQL file
FEED_SQL_FILE="feed.sql"   # Name of your feeds SQL file

# Authenticate with GCP (make sure you have gcloud SDK installed and authenticated)
gcloud auth login

# Set the project
gcloud config set project $PROJECT_ID


# Enable the Cloud SQL Admin API
gcloud services enable sqladmin.googleapis.com


# Create a Cloud SQL instance
gcloud sql instances create $INSTANCE_NAME \
    --database-version=MYSQL_8_0 \
    --cpu=2 \
    --memory=7680MB \
    --region=$REGION

# Set the root password using environment variable
gcloud sql users set-password root \
    --host=% \
    --instance=$INSTANCE_NAME \
    --password=$ROOT_PASSWORD

# Create a user called 'cobra' using environment variable
gcloud sql users create cobra \
    --host=% \
    --instance=$INSTANCE_NAME \
    --password=$COBRA_PASSWORD

# Grant superuser privileges to 'cobra'
gcloud sql connect $INSTANCE_NAME --user=root --quiet << EOF
ALTER USER 'cobra'@'%' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON *.* TO 'cobra'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
EOF

# Optional: Create a database (uncomment if needed)
# DATABASE_NAME="your-database-name"
# gcloud sql databases create $DATABASE_NAME --instance=$INSTANCE_NAME

# Create a database
gcloud sql databases create $DATABASE_NAME --instance=$INSTANCE_NAME

# Execute the SQL files to create the 'builds' and 'feeds' tables
gcloud sql connect $INSTANCE_NAME --user=cobra --database=$DATABASE_NAME --quiet < $BUILDS_SQL_FILE
gcloud sql connect $INSTANCE_NAME --user=cobra --database=$DATABASE_NAME --quiet < $FEED_SQL_FILE


echo "MySQL instance $INSTANCE_NAME created successfully in project $PROJECT_ID with superuser 'cobra' and executed SQL files '$BUILDS_SQL_FILE' and '$FEEDS_SQL_FILE'."


```

### Create a .env file to save your passwords

There are a number of ways to keep passwords out of github. In this case I am just going to add the passes to a .env file and source it 

the file looks like 

```bash
# .env
ROOT_PASSWORD="your-pass"
COBRA_PASSWORD="your-pass"
```

### Run

### Chmod

```bash

chmod +x your-script

```

### Write the sql files used to create the feed and builds tables

I added a submodule that contains my scripts [gh link](https://github.com/justin-napolitano/mysql-config)

#### Builds

```sql
CREATE TABLE builds (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    link VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    generator VARCHAR(255),
    language VARCHAR(10),
    copyright VARCHAR(255),
    lastBuildDate TIMESTAMP,
    atom_link_href VARCHAR(255),
    atom_link_rel VARCHAR(50),
    atom_link_type VARCHAR(50)
);
```

#### Feed

```sql 

CREATE TABLE feed (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    link VARCHAR(255) NOT NULL,
    pubDate TIMESTAMP,
    guid VARCHAR(255),
    description TEXT
);


```

### Run the script

```./yourscript```

The script should work and create your basic files.. I have some more work to do to create an api to update the tables.  