# Notes API
![CI](https://github.com/XCVI1/notes-api/actions/workflows/ci.yml/badge.svg)
![Version](https://img.shields.io/github/v/release/XCVI1/notes-api)

A self-hosted REST API for managing notes, built with FastAPI and PostgreSQL. Includes full CI/CD pipeline with GitHub Actions, Kubernetes deployment and HTTPS via Let's Encrypt.

## Features

- **Notes management**: Create, read, update, and delete notes
- **Authentication**: JWT-based user authentication
- **Public/Private notes**: Control note visibility
- **CI/CD**: Automated testing, security scanning, and deployment via GitHub Actions
- **Multi-stage Docker build**: Optimized image size
- **Kubernetes**: Deployed on k3s with Deployments, Services and Secrets
- **HTTPS**: SSL certificate via Let's Encrypt and Nginx reverse proxy

---

## Project Structure
```
.
├── app/
│   ├── main.py              # Application
│   ├── config.py            # Configuration and settings
│   ├── database.py          # Database connection
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # Authentication
│   └── routers/
│       ├── notes.py         # Notes endpoints
│       └── users.py         # Auth endpoints
├── k8s/
│   ├── api-deployment.yml   # API Deployment and Service
│   ├── postgres-deployment.yml  # PostgreSQL Deployment and Service
│   ├── configmap.yml        # Non-sensitive configuration
│   └── ingress.yml          # Traefik Ingress
├── migrations/              # Alembic migrations
├── nginx/
│   └── nginx.conf           # Nginx reverse proxy config
├── tests/
│   └── test_main.py         # API tests
├── .github/
│   └── workflows/
│       ├── ci.yml           # CI pipeline
│       └── cd.yml           # CD pipeline
├── Dockerfile               # Multi-stage build
├── docker-compose.yml       # Local development
├── docker-compose.prod.yml  # Production deployment
├── alembic.ini              # Alembic configuration
└── requirements.txt
```

---

## Security

Before deployment create a `.env` file with your settings:
```
DATABASE_URL=postgresql://user:password@postgres:5432/notesdb
SECRET_KEY=your-secret-key
```

Generate a secure secret key:
```sh
python3 -c "import secrets; print(secrets.token_hex(32))"
```

---

## Prerequisites

- Docker and Docker Compose
- Python 3.11+
- k3s (for Kubernetes deployment)

---

## Getting Started

### Local Development

1. Clone the repository:
```sh
git clone https://github.com/XCVI1/notes-api.git
cd notes-api
```

2. Create `.env` file with your settings.

3. Start the services:
```sh
docker compose up -d
```

4. Run migrations:
```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
```

5. Open `http://localhost:8090/docs`

### Running Tests
```sh
source venv/bin/activate
pytest tests/ -v
```

---

## API Endpoints

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/` | Root | No |
| GET | `/health` | Health check | No |
| POST | `/auth/register` | Register user | No |
| POST | `/auth/login` | Login | No |
| GET | `/notes/public` | Get public notes | No |
| GET | `/notes/` | Get my notes | Yes |
| POST | `/notes/` | Create note | Yes |
| GET | `/notes/{id}` | Get note | Yes |
| PUT | `/notes/{id}` | Update note | Yes |
| DELETE | `/notes/{id}` | Delete note | Yes |

---

## CI/CD Pipeline

### CI (runs on push to main and pull requests)
```
lint (black, isort, flake8)
    ↓
test (pytest, matrix: Python 3.11, 3.12)
    ↓
build-and-push (Docker Hub)
    ↓
security (Trivy vulnerability scan)
```

### CD (runs after CI completes)
```
deploy-staging (push to main)
    └── update nginx config
    └── apply k8s manifests
    └── kubectl rollout restart
    └── healthcheck

deploy-production (git tag v*)
    └── requires manual approval
    └── update nginx config
    └── apply k8s manifests
    └── kubectl rollout restart
    └── healthcheck
    └── create GitHub Release
```

### GitHub Secrets Required

| Secret | Description |
|---|---|
| `DOCKERHUB_USERNAME` | Docker Hub username |
| `DOCKERHUB_TOKEN` | Docker Hub access token |
| `SSH_HOST` | Server IP address |
| `SSH_USER` | SSH username |
| `SSH_PRIVATE_KEY` | SSH private key |
| `DATABASE_URL` | PostgreSQL connection string |
| `POSTGRES_PASSWORD` | PostgreSQL password |
| `SECRET_KEY` | JWT secret key |
| `KUBECONFIG` | k3s kubeconfig file |

---

## Roadmap

- [x] FastAPI REST API
- [x] JWT authentication
- [x] PostgreSQL + Alembic migrations
- [x] Multi-stage Dockerfile
- [x] Docker Compose for local development
- [x] CI/CD with GitHub Actions
- [x] Security scanning with Trivy
- [x] Nginx reverse proxy
- [x] SSL certificate via Let's Encrypt
- [x] Kubernetes deployment with k3s
- [x] Automatic dependency updates via Dependabot
- [x] GitHub Releases on production deploy