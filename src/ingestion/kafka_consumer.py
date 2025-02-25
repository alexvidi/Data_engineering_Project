import json
import logging
from kafka import KafkaConsumer
import psycopg2
from psycopg2 import sql

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Kafka configuration
KAFKA_BROKER = 'localhost:9092'
KAFKA_TOPIC = 'test-topic'

# PostgreSQL configuration
PG_HOST = 'localhost'
PG_PORT = '5432'
PG_DATABASE = 'products_db'
PG_USER = 'postgres'
PG_PASSWORD = 'password'

def connect_postgres():
    """Establish a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            host=PG_HOST,
            port=PG_PORT,
            database=PG_DATABASE,
            user=PG_USER,
            password=PG_PASSWORD
        )
        logging.info("Connected to PostgreSQL database.")
        return conn
    except Exception as e:
        logging.error(f"Error connecting to PostgreSQL: {e}")
        exit()

def insert_product(cursor, product):
    """Insert product data into PostgreSQL."""
    try:
        insert_query = sql.SQL("""
            INSERT INTO products (title, description, price, brand, category, stock, rating)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """)
        cursor.execute(insert_query, (
            product.get('title'),
            product.get('description'),
            product.get('price'),
            product.get('brand'),
            product.get('category'),
            product.get('stock'),
            product.get('rating')
        ))
        logging.info(f"Inserted product: {product.get('title')}")
    except Exception as e:
        logging.error(f"Error inserting product: {e}")

def main():
    # Initialize Kafka consumer
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='product-consumers',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    # Connect to PostgreSQL
    conn = connect_postgres()
    cursor = conn.cursor()

    # Consume messages from Kafka
    logging.info("Consuming messages from Kafka...")
    try:
        for message in consumer:
            product = message.value
            logging.debug(f"Received message: {product}")
            insert_product(cursor, product)
            conn.commit()
    except KeyboardInterrupt:
        logging.info("Consumer stopped.")
    except Exception as e:
        logging.error(f"Error during consumption: {e}")
    finally:
        cursor.close()
        conn.close()
        consumer.close()
        logging.info("Connections closed.")

if __name__ == '__main__':
    main()





