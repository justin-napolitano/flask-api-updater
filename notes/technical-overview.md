---
slug: github-flask-api-updater-note-technical-overview
id: github-flask-api-updater-note-technical-overview
title: flask-api-updater
repo: justin-napolitano/flask-api-updater
githubUrl: https://github.com/justin-napolitano/flask-api-updater
generatedAt: '2025-11-24T18:36:08.421Z'
source: github-auto
summary: >-
  This repo is a Flask app for updating specific tables in a Google Cloud SQL
  MySQL database. It showcases different connection methods and allows updates
  through REST API endpoints.
tags: []
seoPrimaryKeyword: ''
seoSecondaryKeywords: []
seoOptimized: false
topicFamily: null
topicFamilyConfidence: null
kind: note
entryLayout: note
showInProjects: false
showInNotes: true
showInWriting: false
showInLogs: false
---

This repo is a Flask app for updating specific tables in a Google Cloud SQL MySQL database. It showcases different connection methods and allows updates through REST API endpoints.

## Key Features

- REST API for table updates.
- Supports TCP, Unix socket, and Cloud SQL Python Connector (with IAM auth).
- Kubernetes deployment manifests included.
- Local testing setup with environment variables.

## Quick Start

1. Clone the repo:

    ```bash
    git clone https://github.com/justin-napolitano/flask-api-updater.git
    cd flask-api-updater/src
    ```

2. Set up a virtual environment:

    ```bash
    virtualenv --python=python3 env
    source env/bin/activate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set your environment variables in a `.env` file.

5. Run the app:

    ```bash
    python app.py
    ```

   Access it at `http://127.0.0.1:8080`.

**Gotcha:** Manage sensitive files like `secret.json` carefully.
