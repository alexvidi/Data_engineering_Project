from kafka import KafkaProducer
import json
import requests
import time

"""
Kafka Producer Script

This script fetches product data from the DummyJSON API and sends it to a Kafka topic.
The producer connects to a local Kafka broker and streams product data in real-time.
"""

# Kafka configuration
KAFKA_BROKER = 'localhost:9092'  # Kafka broker address
KAFKA_TOPIC = 'test-topic'       # Kafka topic name

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize data to JSON
)

def fetch_data(limit=1000):
    """
    Fetches product data from the DummyJSON API.

    Args:
        limit (int): The total number of products to fetch.

    Returns:
        list: A list of product dictionaries.
    """
    url = 'https://dummyjson.com/products'
    products = []
    batch_size = 100  # Maximum allowed by the API per request
    total_fetched = 0

    while total_fetched < limit:
        params = {
            'limit': batch_size,
            'skip': total_fetched
        }
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            batch = response.json().get('products', [])
            if not batch:
                # No more products available
                break
            products.extend(batch)
            total_fetched += len(batch)
            print(f"Fetched {total_fetched} products so far...")
        else:
            print(f"Error fetching data: {response.status_code}")
            break

    return products[:limit]  # Ensure the limit is not exceeded

def send_to_kafka(data):
    """
    Sends product data to the Kafka topic.

    Args:
        data (list): List of product dictionaries to send.
    """
    for idx, item in enumerate(data, start=1):
        print(f"Sending ({idx}/{len(data)}): {item['title']}")
        producer.send(KAFKA_TOPIC, item)
        time.sleep(0.01)  # Simulate real-time streaming

if __name__ == '__main__':
    print("Fetching data from DummyJSON API...")
    products = fetch_data(limit=1000)
    
    if products:
        print(f"Fetched {len(products)} products. Sending to Kafka...")
        send_to_kafka(products)
        producer.flush()  # Ensure all messages are sent
        print("All messages sent to Kafka.")
    else:
        print("No data fetched. Exiting.")

