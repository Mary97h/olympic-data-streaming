from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings

print("Setting up the environment")
env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(1)

settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
t_env = StreamTableEnvironment.create(env, environment_settings=settings)

print("Registering the mysql cdc connector jar")
t_env.get_config().get_configuration().set_string(
    "pipeline.jars", "file:///opt/flink/lib/flink-sql-connector-mysql-cdc-2.3.0.jar"
)

print("Creating cdc source table 'players_cdc'")
t_env.execute_sql("""
CREATE TABLE players_cdc (
  id INT,
  name STRING,
  nationality STRING,
  score INT,
  PRIMARY KEY (id) NOT ENFORCED
) WITH (
  'connector' = 'mysql-cdc',
  'hostname' = 'mysql',
  'port' = '3306',
  'username' = 'root',
  'password' = 'mary1234',
  'database-name' = 'olympics',
  'table-name' = 'players',
  'scan.startup.mode' = 'initial',
  'server-id' = '5001-6000',
  'server-time-zone' = 'UTC'
)
""")

print(" the print sink table")
t_env.execute_sql("""
CREATE TABLE print_sink (
  id INT,
  name STRING,
  nationality STRING,
  score INT
) WITH (
  'connector' = 'print'
)
""")

print("submitiing the job")
t_env.execute_sql("""
INSERT INTO print_sink
SELECT * FROM players_cdc
""").wait()
