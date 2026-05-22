# Kubernetes ML Deployment with CI/CD

Deploys the ML Serving API on Kubernetes with automated CI/CD via GitHub Actions.

## Stack
- **Orchestration**: Kubernetes (Minikube)
- **App**: FastAPI + scikit-learn (fraud detection)
- **Database**: PostgreSQL
- **Auto-scaling**: HPA (2–10 replicas)
- **CI/CD**: GitHub Actions + DockerHub

## Architecture
GitHub Push → GitHub Actions → Docker Build → DockerHub → Kubernetes

## Run Locally
```bash
minikube start --driver=docker
kubectl apply -f k8s/
minikube service ml-serving-api --url
```

## Test
```bash
curl -X POST http://<URL>/predict \
  -H "Content-Type: application/json" \
  -d '{"amount": 150.00, "hour": 14, "day_of_week": 2, "distance_from_home": 5.3}'
```
