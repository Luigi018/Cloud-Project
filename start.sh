#!/bin/bash

# Crea il cluster GKE
gcloud container clusters create sensor-cluster \
    --zone us-central1-a \
    --num-nodes 5 \
    --enable-ip-alias

# Ottiene le credenziali del cluster
gcloud container clusters get-credentials sensor-cluster \
    --zone us-central1-a \
    --project cloud-project-433315

# Costruisce le immagini Docker
docker build -f Dockerfile.server -t gcr.io/cloud-project-433315/server:latest .
docker build -f Dockerfile.client -t gcr.io/cloud-project-433315/client:latest .

# Pusha le immagini nel container registry
docker push gcr.io/cloud-project-433315/server:latest
docker push gcr.io/cloud-project-433315/client:latest

# Applica le configurazioni di deployment su Kubernetes
kubectl apply -f server-deployment.yaml
kubectl apply -f client-deployment.yaml
