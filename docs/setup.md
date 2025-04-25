# Setup Guide

This document provides detailed instructions for setting up the Olympic Data Streaming Platform in different environments.

## Local Development Environment

### Docker Setup

1. Install Docker and Docker Compose
2. Clone the repository:

   git clone https://github.com/Mary97h/olympic-data-streaming.git
   cd olympic-data-streaming

3. Download required JAR files:

   mkdir -p docker/shared
   wget https://repo1.maven.org/maven2/org/apache/flink/flink-sql-connector-kafka/3.0.1-1.17/flink-sql-connector-kafka-3.0.1-1.17.jar -P docker/shared/
   wget https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.3.1/kafka-clients-3.3.1.jar -P docker/shared/

4. Start the Docker services:
   cd docker
   docker-compose up -d

5. Configure the Flink JobManager:

   docker exec -it $(docker ps | grep jobmanager | awk '{print $1}') bash
   apt update && apt install -y python3 python3-pip
   ln -s /usr/bin/python3 /usr/bin/python
   export PYFLINK_PYTHON=/usr/bin/python
   mkdir -p /opt/flink/pythonfiles
   touch /opt/flink/pythonfiles/**init**.py
   pip install kafka-python
   pip install apache-flink
   exit

6. Copy scripts to the Flink container:

   docker cp src/operators/operators.py $(docker ps | grep jobmanager | awk '{print $1}'):/opt/flink/pythonfiles/
   docker cp src/kafka/kafka_setup.py $(docker ps | grep jobmanager | awk '{print $1}'):/opt/flink/pythonfiles/
   docker cp src/flink/flink_job.py $(docker ps | grep jobmanager | awk '{print $1}'):/opt/flink/pythonfiles/
   docker cp tests/test_olympic_pipeline.py $(docker ps | grep jobmanager | awk '{print $1}'):/opt/flink/pythonfiles/
   docker cp tests/test_task2.py $(docker ps | grep jobmanager | awk '{print $1}'):/opt/flink/pythonfiles/

7. Run the tests and scripts:

   docker exec -it $(docker ps | grep jobmanager | awk '{print $1}') python3 -m unittest -v /opt/flink/pythonfiles/test_olympic_pipeline.py
   docker exec -it $(docker ps | grep jobmanager | awk '{print $1}') python3 /opt/flink/pythonfiles/kafka_setup.py
   docker exec -it $(docker ps | grep jobmanager | awk '{print $1}') /opt/flink/bin/flink run -py /opt/flink/pythonfiles/flink_job.py

8. Check the results in the TaskManager logs:

   docker logs $(docker ps | grep taskmanager | awk '{print $1}')

## Kubernetes Deployment

### Minikube Setup

1. Install Minikube and start the cluster:

   ```bash
   minikube start --driver=docker
   ```

2. Apply the Flink cluster configurations:

   ```bash
   kubectl apply -f kubernetes/flink/jobmanager-deployment.yaml
   kubectl apply -f kubernetes/flink/jobmanager-service.yaml
   kubectl apply -f kubernetes/flink/taskmanager-deployment.yaml
   ```

3. Set up MySQL with CDC enabled:

   ```bash
   kubectl apply -f kubernetes/mysql/mysql-config.yaml
   kubectl apply -f kubernetes/mysql/mysql-deployment.yaml
   ```

4. Verify that all pods are running:

   ```bash
   kubectl get pods
   ```

5. Set up the database schema:

   ```bash
   kubectl exec -it $(kubectl get pods | grep mysql | awk '{print $1}') -- bash
   mysql -u root -p
   # Enter password: mary1234

   USE olympics;

   CREATE TABLE players (
     id INT PRIMARY KEY AUTO_INCREMENT,
     name VARCHAR(50),
     nationality VARCHAR(50),
     score INT
   );

   INSERT INTO players (name, nationality, score) VALUES
   ('Alex', 'Austria', 7),
   ('Peter', 'US', 2),
   ('Josef', 'US', 8),
   ('Max', 'Austria', 4),
   ('Peter', 'US', 2);

   exit
   exit
   ```

6. Create and run the Flink CDC job:

   ```bash
   kubectl create configmap flink-cdc-script --from-file=src/flink/flink_cdc_job.py
   kubectl apply -f kubernetes/jobs/flink-cdc-job.yaml
   ```

7. Monitor the job logs:

   ```bash
   kubectl logs -f $(kubectl get pods | grep flink-cdc-job | awk '{print $1}')
   ```

8. Test database change capture:

   ```bash
   kubectl exec -it $(kubectl get pods | grep mysql | awk '{print $1}') -- mysql -u root -p
   # Enter password: mary1234

   USE olympics;
   INSERT INTO players (name, nationality, score) VALUES ('Mary', 'Italy', 9);
   UPDATE players SET score = 10 WHERE name = 'Alex';
   DELETE FROM players WHERE name = 'Peter' LIMIT 1;

   exit
   ```

9. View the change events in the TaskManager logs:
   ```bash
   kubectl logs -f $(kubectl get pods | grep taskmanager | awk '{print $1}')
   ```

## Troubleshooting

### Common Docker Issues

- **Container not starting**: Check logs with `docker logs <container-id>`
- **Network issues**: Ensure all services can communicate by checking the Docker network with `docker network inspect`
- **PyFlink import errors**: Make sure all Python dependencies are installed in the container

### Common Kubernetes Issues

- **Pod in CrashLoopBackOff**: Check logs with `kubectl logs <pod-name>`
- **ConfigMap not found**: Verify the ConfigMap exists with `kubectl get configmap`
- **Flink job not starting**: Check Flink JobManager UI by port-forwarding: `kubectl port-forward svc/flink-jobmanager 8081:8081`
