# 🔄 CI/CD Pipeline with Docker, Kubernetes & GitHub Actions

![Docker](https://img.shields.io/badge/Docker-24.0+-blue?logo=docker)
![Kubernetes](https://img.shields.io/badge/Kubernetes-1.28+-326CE5?logo=kubernetes)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-CI%2FCD-2088FF?logo=githubactions)
![Helm](https://img.shields.io/badge/Helm-3.12+-0F1689?logo=helm)
![Python](https://img.shields.io/badge/Python-3.11+-yellow?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask)

## 📋 Overview

A production-grade **CI/CD pipeline** that automates the build, test, and deployment lifecycle of a **Python Flask microservices** application. Uses **Docker** for containerization, **Kubernetes** for orchestration, and **GitHub Actions** for continuous integration and deployment.

## 🏗️ Architecture

```
Developer Push → GitHub Actions CI Pipeline
                    │
    ┌───────────────┼───────────────┐
    ▼               ▼               ▼
  Lint &         Unit Tests     Security
  Format         & Coverage     Scanning
    │               │               │
    └───────────────┼───────────────┘
                    ▼
            Docker Build
         (Multi-stage Image)
                    │
                    ▼
          Push to Registry
         (GHCR / DockerHub)
                    │
                    ▼
         Kubernetes Deploy
        (Helm Chart + Kustomize)
                    │
          ┌────────┴────────┐
          ▼                 ▼
       Dev Cluster     Prod Cluster
     (Auto-deploy)   (Manual approval)
```

## 📁 Project Structure

```
cicd-docker-kubernetes/
├── app/
│   ├── service1/              # User Service microservice
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   └── service2/              # Product Service microservice
│       ├── app.py
│       ├── requirements.txt
│       └── Dockerfile
├── tests/
│   ├── test_service1.py
│   └── test_service2.py
├── k8s/
│   ├── base/                  # Base Kubernetes manifests
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── kustomization.yaml
│   └── overlays/
│       ├── dev/               # Dev environment overrides
│       └── prod/              # Prod environment overrides
├── helm/myapp/               # Helm chart
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
├── .github/workflows/
│   ├── ci.yml                # CI pipeline
│   └── cd.yml                # CD pipeline
├── docker-compose.yml        # Local development
├── Makefile                  # Automation commands
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- kubectl & minikube (or any K8s cluster)
- Helm 3
- Python 3.11+

### Local Development
```bash
# Start all services locally
docker-compose up --build

# Run tests
make test

# Deploy to local Kubernetes
make deploy-dev
```

### CI/CD Pipeline
The pipeline triggers automatically on:
- **Push to `main`** → Full CI + Deploy to dev
- **Push to `release/*`** → Full CI + Deploy to prod (with approval)
- **Pull Requests** → CI checks only

## 🔑 Key Features

### Multi-stage Docker Builds
- Optimized images (~50MB vs ~400MB)
- Separated build and runtime stages
- Non-root container user

### Automated Testing
- Unit tests with pytest
- 80%+ code coverage enforcement
- Integration tests with Docker Compose

### Security Scanning
- Docker image vulnerability scanning (Trivy)
- Python dependency audit (safety)
- Secret detection in code

### Kubernetes Deployment
- Rolling updates with zero downtime
- Horizontal Pod Autoscaling
- Health checks (liveness + readiness probes)
- Resource limits and requests

## 📊 Pipeline Stages

| Stage | Tools | Description |
|-------|-------|-------------|
| **Lint** | flake8, black | Code style enforcement |
| **Test** | pytest, coverage | Unit tests with coverage |
| **Build** | Docker | Multi-stage image build |
| **Scan** | Trivy, safety | Security vulnerability scan |
| **Push** | GHCR | Push to container registry |
| **Deploy** | Helm, kubectl | Deploy to Kubernetes |

## 👤 Author
**Tushar Kumar** — [GitHub](https://github.com/sparrow000iv) | [LinkedIn](https://www.linkedin.com/in/tushar-kumar-737a6b303/)
