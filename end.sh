#!/bin/bash

# Elimina tutti i deployment nel cluster Kubernetes
kubectl delete deployment --all

# Elimina il cluster GKE
gcloud container clusters delete sensor-cluster --zone us-central1-a --quiet
