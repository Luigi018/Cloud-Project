import os
import time
import json
import uuid
import random
from google.cloud import pubsub_v1

service_account_file = "cloud-project-433315-ab9bd94595a6.json"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_file

project_id = "cloud-project-433315"
topic_id = "sensor-data"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

client_id = str(uuid.uuid4())

current_temperature = 20.0  # Temperatura iniziale

def publish_sensor_data():
    global current_temperature 
    while True:
        temperature_change = random.uniform(-3, 3)  # Variazione casuale tra -3 e 3
        current_temperature = round(current_temperature + temperature_change, 2)

        current_temperature = max(15, min(50, current_temperature)) # Range temperatura 15-50
        
        # La pressione aumenta di 0.05 bar per ogni grado sopra i 20 gradi Celsius e diminuisce sotto i 20 gradi
        base_pressure = 2.0  # Pressione iniziale
        pressure = round(base_pressure + (current_temperature - 20) * 0.05, 2)

        sensor_data = {
            "client_id": client_id,
            "temperature": current_temperature,
            "pressure": pressure
        }

        data = json.dumps(sensor_data).encode("utf-8")

        # Pubblica il messaggio su Pub/Sub
        future = publisher.publish(topic_path, data)
        print(f"Published {sensor_data}, message ID: {future.result()}")

        time.sleep(5)

if __name__ == "__main__":
    publish_sensor_data()
