# Data Engineering Project

The Data Engineering Project focuses on building a real-time data ingestion pipeline leveraging Apache Kafka for event streaming and PostgreSQL as the storage backend. This project simulates a data ingestion system where producers send data to Kafka topics, and consumers process this data and store it in a relational database.

The entire architecture is containerized using Docker Compose, enabling easy setup and scalability. The system consists of:

- Kafka Producer: Simulates real-time data by sending JSON messages to a Kafka topic.
- Kafka Consumer: Listens to the Kafka topic, processes incoming messages, and inserts them into a PostgreSQL database.
- PostgreSQL Database: Acts as persistent storage for the processed data.
- Docker Compose: Orchestrates Kafka, Zookeeper, and PostgreSQL services.

This project demonstrates key concepts in data engineering, such as event-driven architecture, message queuing, data streaming, and integration between streaming platforms and databases.

##  Project Structure

```
Data_engineering_Project/
├── docker-compose.yml        # Docker Compose configuration for Kafka, Zookeeper, and PostgreSQL
├── src/
│   └── ingestion/
│       ├── kafka_producer.py # Kafka producer script
│       └── kafka_consumer.py # Kafka consumer script
├── venv/                     # Python virtual environment
├── .gitignore                # Git ignore file
└── README.md                 # Project documentation
```

## Getting Started

### Prerequisites

- Docker & Docker Compose
- Python 3.x

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/alexvidi/Project-ETL-kafka-Postgres-Docker.git
   cd Data_engineering_Project
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start services with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

## Usage

1. **Run Kafka Producer:**
   ```bash
   python src/ingestion/kafka_producer.py
   ```

2. **Run Kafka Consumer:**
   ```bash
   python src/ingestion/kafka_consumer.py
   ```

3. **Check PostgreSQL Database:**
   Connect to the PostgreSQL instance using pgAdmin or any SQL client:
   ```sql
   SELECT * FROM public.products;
   ```

## Configuration

- **Kafka Broker:** `localhost:9092`
- **Kafka Topic:** `test-topic`
- **PostgreSQL:**
  - Host: `localhost`
  - Port: `5432`
  - Database: `products_db`
  - User: `postgres`
  - Password: `xxxxxxx`

## Features

- Kafka-based data ingestion pipeline.
- PostgreSQL for persistent storage.
- Docker Compose for container orchestration.
- Modular and scalable architecture.

## License

This project is licensed under the MIT License.

---


