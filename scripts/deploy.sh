#!/bin/bash
set -e

# Deploy the GitOps demo application using kubectl
echo "Deploying GitOps demo application..."

# Create namespace if it doesn't exist
kubectl create namespace default --dry-run=client -o yaml | kubectl apply -f -

# Apply Kubernetes manifests
echo "Applying deployment manifest..."
kubectl apply -f deploy/deployment.yaml

echo "Applying service manifest..."
kubectl apply -f deploy/service.yaml

# Wait for deployment to be ready
echo "Waiting for deployment to be ready..."
kubectl rollout status deployment/gitops-demo-app --timeout=300s

# Show deployment status
echo "Deployment completed successfully!"
kubectl get pods -l app=gitops-demo
kubectl get services gitops-demo-service

echo "Application is now running. Use 'kubectl port-forward service/gitops-demo-service 8080:80' to access it locally."
