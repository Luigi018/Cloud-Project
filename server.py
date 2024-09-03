from google.cloud import pubsub_v1
from elasticsearch import Elasticsearch
import json
import os
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

service_account_file = "cloud-project-433315-ab9bd94595a6.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_file

project_id = "cloud-project-433315"
subscription_id = "sensor-data-sub"

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

cloud_id = "My_deployment:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyQ5OGNjNTRiMzIwODI0NGJmYjI4OGUzYjBkYzU2NzNhMiRhOGVhYWU5NDVhNzg0NzY2YjQxZDUzMjQzYmY0NDk5Mg=="
api_key = ""

es = Elasticsearch(
    cloud_id=cloud_id,
    api_key=api_key
)

client_id_map = {}
next_index_number = 1

def clear_elasticsearch_indices():
    global client_id_map, next_index_number
    try:
        es.indices.delete(index='*')
        logging.info("Tutti gli indici di Elasticsearch sono stati cancellati con successo.")
        client_id_map = {}
        next_index_number = 1
    except Exception as e:
        logging.error(f"Errore durante la cancellazione degli indici: {e}")

try:
    response = es.info()
    print("Connesso a Elasticsearch Cloud con successo!")
    print(response)
except Exception as e:
    print(f"Errore di connessione: {e}")

def callback(message):
    global next_index_number
    try:
        raw_data = message.data.decode('utf-8')
        logging.info(f"Raw message data: {raw_data}")
        
        sensor_data = json.loads(raw_data)
        client_id = sensor_data.get("client_id", "unknown")
        
        if client_id not in client_id_map:
            # Mappa il nuovo client_id a un numero sequenziale
            client_id_map[client_id] = next_index_number
            next_index_number += 1
        
        client_number = client_id_map[client_id]
        index_name = f"sensor-data-{client_number}"
        
        sensor_data['timestamp'] = datetime.utcnow().isoformat()
        
        es.index(index=index_name, body=sensor_data)
        logging.info(f"Indexed data from client {client_id} into index {index_name}: {sensor_data}")
        
        message.ack()
    except json.JSONDecodeError as e:
        logging.error(f"JSON decode error: {e}")
        message.nack()
    except Exception as e:
        logging.error(f"Error during message processing: {e}")
        message.nack()

def main():
    # Pulisce tutti gli indici di Elasticsearch all'avvio
    clear_elasticsearch_indices()
    
    streaming_pull_future = subscriber.subscribe(subscription_path, callback)
    logging.info(f"Listening for messages on {subscription_path}...")

    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()

if __name__ == "__main__":
    main()
