# flask-api-updater

A Python Flask application designed to update specific tables in a Google Cloud SQL MySQL database. This project demonstrates connecting to Cloud SQL using multiple connection methods and automates updating database records via API endpoints.

---

## Features

- Flask-based REST API for updating database tables.
- Supports multiple Cloud SQL connection methods: TCP, Unix socket, and Cloud SQL Python Connector with optional IAM authentication.
- Kubernetes deployment manifests for service and deployment.
- Local testing setup with environment variables and service account credentials.

---

## Tech Stack

- Python 3.10
- Flask
- SQLAlchemy
- Google Cloud SQL (MySQL)
- Google Cloud SQL Python Connector
- Kubernetes (GKE) manifests
- Docker

---

## Getting Started

### Prerequisites

- Python 3.10+
- Google Cloud project with Cloud SQL instance
- Service account with Cloud SQL Client permissions
- Docker (for container builds)
- Kubernetes cluster (optional, for deployment)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/justin-napolitano/flask-api-updater.git
cd flask-api-updater/src
```

2. Create and activate a virtual environment:

```bash
virtualenv --python=python3 env
source env/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set environment variables (example `.env`):

```bash
export GOOGLE_APPLICATION_CREDENTIALS='secret.json'
export INSTANCE_CONNECTION_NAME='your-project:region:instance'
export DB_USER='your-db-user'
export DB_PASS='your-db-password'
export DB_NAME='your-db-name'
# Optionally set INSTANCE_HOST or INSTANCE_UNIX_SOCKET depending on connection method
```

### Running Locally

```bash
python app.py
```

Open your browser and navigate to `http://127.0.0.1:8080` to verify the app is running.

---

## Project Structure

```
flask-api-updater/
├── README.md
├── index.md
├── src/
│   ├── app.py                    # Flask app with API endpoints
│   ├── main.py                   # Cloud Functions HTTP handler
│   ├── connect_connector.py      # Cloud SQL Python Connector connection
│   ├── connect_connector_auto_iam_authn.py # Connector with IAM auth
│   ├── connect_tcp.py            # TCP connection method
│   ├── connect_unix.py           # Unix socket connection method
│   ├── connection_test.py        # Pytest tests for app
│   ├── service.yaml              # Kubernetes Service manifest
│   ├── deployment.yaml           # Kubernetes Deployment manifest
│   ├── app.standard.yaml         # App Engine standard environment config
│   ├── app.flexible.yaml         # App Engine flexible environment config
│   ├── service-account.yaml      # Kubernetes service account manifest
│   ├── cloudbuild.yaml           # Cloud Build config for production
│   ├── cloudbuild-dev.yaml       # Cloud Build config for dev
│   ├── README.md                 # Cloud SQL connection instructions
│   └── secret.json               # Service account credentials (example)
```

---

## Future Work / Roadmap

- Complete and extend API endpoints for updating additional tables.
- Integrate Google Cloud Secret Manager for secure credential handling.
- Add comprehensive unit and integration tests.
- Automate deployment with CI/CD pipelines.
- Improve error handling and logging.
- Add support for additional database engines or cloud providers.

---

*Note: Some files like `secret.json` contain sensitive information and should be managed securely and excluded from public repositories.*