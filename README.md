# Cloud-Project

The command builds a Docker image for the server or client using the specified Dockerfile and tags it with the latest version for deployment to Google Container Registry.

    docker build -f Dockerfile.server|client -t 
    gcr.io/cloud-project-433315/server|client:latest .

The command uploads the Docker image tagged as latest for the server or client to the Google Container Registry.

    docker push gcr.io/cloud-project-433315/server|client:latest

The command is used to deploy or update the configuration of a Kubernetes application, which defines the deployment settings for the server or client.

    kubectl apply -f server|client-deployment.yaml

The command creates a new Google Kubernetes Engine (GKE) cluster named "sensor-cluster" in the us-central1-a.

    gcloud container clusters create sensor-cluster \
    --zone us-central1-a \
    --num-nodes 5 \
    --enable-ip-alias

The command configures kubectl to use the credentials for the "sensor-cluster" in the us-central1-a zone, allowing you to interact with the cluster in the cloud-project-433315 project.

    gcloud container clusters get-credentials sensor-cluster \
    --zone us-central1-a \
    --project cloud-project-433315

To run all the above scripts, you can use the following command:

    ./start.sh

To delete the deployments and stop the cluster, you can use:

    ./end.sh

To run the code locally, first install the required dependencies by executing:

    pip install -r requirements.txt

Then, start the server and client with the following commands:

    python3 server.py
    python3 client.py

To test it on your project, modify the service account in the JSON file, along with the project_id, subscription_id, cloud_id, and api_key (for Elasticsearch) in the server configuration. In the client configuration, only change the project_id and topic_id.

For more details, please read Relazione.pdf or translate it if you're not italian.

Credentials have been removed for security reasons. Please request the correct credentials from the owner to ensure proper functionality.

