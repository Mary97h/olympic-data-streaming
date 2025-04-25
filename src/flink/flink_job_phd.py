from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(1)
env_settings = EnvironmentSettings.in_streaming_mode()
t_env = StreamTableEnvironment.create(env, environment_settings=env_settings)

t_env.get_config().set("pipeline.jars", "file:///opt/flink/custom-jars/flink-sql-connector-kafka-3.0.1-1.17.jar")

print("Creating Kafka source table")
source_ddl = """
CREATE TABLE kafka_source (
    type STRING,
    data STRING
) WITH (
    'connector' = 'kafka',
    'topic' = 'olympic_data',
    'properties.bootstrap.servers' = 'kafka:9092',
    'properties.group.id' = 'olympic_group',
    'format' = 'json',
    'scan.startup.mode' = 'earliest-offset'
)
"""
t_env.execute_sql(source_ddl)

print("Creating print sink table...")
sink_ddl = """
CREATE TABLE results_sink (
    message STRING
) WITH (
    'connector' = 'print'
)
"""
t_env.execute_sql(sink_ddl)

print("verify connectivity...")
statement_set = t_env.create_statement_set()
statement_set.add_insert_sql("""
INSERT INTO results_sink
SELECT CONCAT('Type: ', type, ', Data: ', data) AS message
FROM kafka_source
""")

job_client = statement_set.execute().get_job_client()
if job_client:
    print(f"Job submitted with JobID: {job_client.get_job_id()}")
    try:
        print("Streaming job is running")
        job_client.get_job_execution_result().result()
    except Exception as e:
        print(f"Job execution failed: {e}")
else:
    print("Failed to get job client")
