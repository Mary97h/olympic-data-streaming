# Olympic Data Streaming Platform

A real-time data processing system for Olympic event statistics using Apache Flink, Kafka, and Kubernetes.

## Overview

This project demonstrates a scalable data pipeline for processing Olympic athlete performance metrics in real-time. It showcases:

- Stream processing with Apache Flink
- Message queue management with Apache Kafka
- Containerization with Docker
- Orchestration with Kubernetes
- Change Data Capture (CDC) for database streaming

## Architecture

![Architecture Diagram](docs/architecture_diagram.png)

The system consists of three main components:

1. **Data Ingestion** - Kafka receives Olympic event data and distributes it to processing nodes
2. **Stream Processing** - Flink operators perform real-time analytics on athlete performance data
3. **Deployment** - Both Docker Compose and Kubernetes configurations are provided for flexible deployment

## Key Features

- Real-time athlete performance analytics
- Nationality-based grouping and statistics
- Top performer identification
- Duplicate athlete detection
- Change Data Capture from MySQL
- Scalable processing with Flink's distributed architecture

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Kubernetes cluster (Minikube for local testing)
- Python 3.9+

### Docker Setup

1. Clone the repository and navigate to the docker directory:

```bash
git clone https://github.com/Mary97h/olympic-data-streaming.git
cd olympic-data-streaming/docker
```

2. Download required JAR files:

```bash
mkdir -p shared
wget https://repo1.maven.org/maven2/org/apache/flink/flink-sql-connector-kafka/3.0.1-1.17/flink-sql-connector-kafka-3.0.1-1.17.jar -P shared/
wget https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.3.1/kafka-clients-3.3.1.jar -P shared/
```

3. Start the services:

```bash
docker-compose up -d
```

4. Run the sample data processor:

```bash
docker exec -it <jobmanager-container-id> python3 /opt/flink/pythonfiles/kafka_setup.py
```

### Kubernetes Setup

1. Start Minikube:

```bash
minikube start --driver=docker
```

2. Apply Kubernetes configurations:

```bash
kubectl apply -f kubernetes/flink/
kubectl apply -f kubernetes/mysql/
```

3. Create the Flink job:

```bash
kubectl create configmap flink-cdc-script --from-file=src/flink/flink_cdc_job.py
kubectl apply -f kubernetes/jobs/flink-cdc-job.yaml
```

## Pipeline Operators

The system includes several operators that process the data stream:

- **Data Join** - Combines athlete names, scores, and nationalities
- **Duplicate Check** - Removes duplicate athletes from the stream
- **Nationality Grouping** - Groups athletes by country
- **Average Score Calculation** - Computes average scores per nationality
- **Highest Score Retrieval** - Identifies top performers per nationality
- **Top Three Identification** - Extracts the three highest-scoring athletes overall

## Testing

Run the test suite to verify operators:

```bash
python -m unittest tests/test_olympic_pipeline.py
python -m unittest tests/test_task2.py
```

## Author

Mary Hannoush - [LinkedIn](https://www.linkedin.com/in/maryhannoush) - maryhannoush3@gmail.com# olympic-data-streaming
