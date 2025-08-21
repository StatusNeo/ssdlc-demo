# SSDLC Demo

A minimal FastAPI application demonstrating a Secure SDLC (SSDL) with multiple security controls integrated into CI/CD.

## Features
- Health and Echo endpoints (`/health`, `/echo`)
- Structured JSON logging
- Unit tests with `pytest` and coverage threshold (>=80%)
- Tooling via pre-commit: Black, isort, Flake8, Mypy, Bandit, detect-secrets
- SCA: Dependabot for pip, Docker, Terraform, GitHub Actions
- SAST: SonarCloud via GitHub Action
- IaC: Terraform for ECR, ECS Fargate, ALB, Security Groups + Checkov scan
- Container security: Trivy scan in pipeline
- DAST: OWASP ZAP baseline scan workflow

## Getting Started

### Requirements
- Python 3.11+
- Docker (optional for container runs)

### Install and Run
```bash
python -m pip install -U pip
python -m pip install -e .[dev]
make run
```
Open http://127.0.0.1:8000/docs

### With Docker Compose
```bash
docker compose up --build
```

### Tests and Quality
```bash
make format
make lint
make type-check
make test
make security-scan
make precommit
```

## CI/CD and Security Gates
- `ci.yml`: runs formatting, linting, typing, bandit, pip-audit, tests, coverage, SonarCloud
- `deploy.yml`: on main, builds image, scans with Trivy, pushes to ECR, Terraform apply with OIDC
- `dast-zap.yml`: nightly + PR ZAP baseline scan against ephemeral container
- Checkov is run over `infra/` as part of CI

## Terraform Deploy (AWS)
Variables (see `infra/variables.tf`):
- `region` (default `us-east-1`)
- `name` (default `ssdlc-demo`)
- `image_tag` (set to Docker tag pushed to ECR)

Apply:
```bash
cd infra
terraform init
terraform plan -var="image_tag=<tag>"
terraform apply -auto-approve -var="image_tag=<tag>"
```

## Backlog
- RASP integration placeholder
- Application fuzzing hooks (e.g., `pytest` property-based tests / fuzzers) 