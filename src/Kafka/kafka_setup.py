import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from kafka import KafkaAdminClient, KafkaProducer, KafkaConsumer
from kafka.admin import NewTopic
import json
import time
from operators import * 

def create_partitioned_topic(bootstrap_servers='kafka:9092', topic_name='olympic_data', num_partitions=3):
    """Create a Kafka topic with multiple partitions for better performance"""
    admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
    
    topics = admin_client.list_topics()
    if topic_name in topics:
        print(f'Topic {topic_name} already exists')
        admin_client.close()
        return
    
    
    topic = NewTopic(
        name=topic_name,
        num_partitions=num_partitions,
        replication_factor=1
    )
    
    admin_client.create_topics([topic])
    print(f'Successfully created topic {topic_name} with {num_partitions} partitions')
    admin_client.close()

def produce_sample_data(bootstrap_servers='kafka:9092', topic_name='olympic_data'):
    """Send sample Olympic data to Kafka topic"""
    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    
    sample_data = [
        {'type': 'name', 'data': ['Alex', 'Peter', 'Josef', 'Max', 'Peter']},
        {'type': 'score', 'data': [7, 2, 8, 4, 2]},
        {'type': 'nationality', 'data': ['Austria', 'US', 'US', 'Austria', 'US']}
    ]
    
    for record in sample_data:
        key = record['type'].encode('utf-8')
        producer.send(topic_name, value=record, key=key)
        print(f'Sent {record["type"]} data to Kafka')
    
    producer.flush()
    producer.close()

def consume_and_process_data(bootstrap_servers='kafka:9092', topic_name='olympic_data'):
    """Consume data from Kafka topic and run through the pipeline"""
    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers=bootstrap_servers,
        auto_offset_reset='earliest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        group_id='olympic-pipeline-group'
    )
    
    
    names = None
    scores = None
    nationalities = None
    
    print('Waiting for messages')
    for _ in range(3): 
        msg = next(consumer)
        print(f'Received message from partition {msg.partition}: {msg.value}')
        
        if msg.value['type'] == 'name':
            names = msg.value['data']
        elif msg.value['type'] == 'score':
            scores = msg.value['data']
        elif msg.value['type'] == 'nationality':
            nationalities = msg.value['data']
    
    if names and scores and nationalities:
        print('\nProcessing data')
        
        joined_data = data_join_operator(names, scores, nationalities)
        unique_data = duplicate_check_operator(joined_data)
        grouped_data = data_grouping_by_nationality_operator(unique_data)
        avg_scores = average_score_calculation_operator(grouped_data)
        top_players = highest_score_retrieval_operator(grouped_data)
        
        print('\nResults:')
        nationality_stats = display_average_and_top_player_operator(avg_scores, top_players)
        for stat in nationality_stats:
            print(f'{stat["nationality"]}: Avg={stat["average_score"]:.1f}, Top={stat["top_player"]}')
            
        overall_stats = overall_best_group_and_top_three_operator(grouped_data, avg_scores)
        print(f'\nBest Group: {overall_stats["best_group"]["nationality"]} (Avg={overall_stats["best_group"]["average_score"]:.1f})')
        print(f'Top Three: {", ".join(overall_stats["top_three_individuals"])}')
    
    consumer.close()

def run_kafka_demo():
    """Run the complete Kafka integration demo"""
    create_partitioned_topic()

    produce_sample_data()
    
    time.sleep(1) 
    consume_and_process_data()

if __name__ == '__main__':
    run_kafka_demo()
