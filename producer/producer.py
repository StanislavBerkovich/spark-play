from confluent_kafka import Producer
import json
import random
from datetime import datetime
import time

KAFKA_BOOTSTRAP_SERVERS = 'kafka:9092'  # Replace with your Kafka bootstrap servers
TOPIC_NAME = 'user_registration'  # Replace with your Kafka topic name


def delivery_report(err, msg):
    """Callback function to handle the delivery report from Kafka."""
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def generate_fake_data(id):
    """Generate fake data for the Kafka messages."""
    # Replace this with your own logic to generate the desired fake data
    fake_data = {
        "user_id": id,
        "name": "John Doe",
        "email": "john.doe@example.com",
        "timestamp": str(datetime.now())
    }
    return json.dumps(fake_data)

def produce_fake_messages(producer, topic, num_messages):
    """Produce fake messages to the specified Kafka topic."""
    for id in range(num_messages):
        fake_data = generate_fake_data(id)
        producer.produce(topic, value=fake_data, callback=delivery_report)
        producer.flush()

def main():
    # Configure Kafka producer
    producer_config = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS
    }
    producer = Producer(producer_config)

    # Produce fake messages
    num_messages = 1000  # Number of fake messages to produce
    produce_fake_messages(producer, TOPIC_NAME, num_messages)

    # Flush and wait for all messages to be sent
    producer.flush()

    # Wait for a few seconds before closing the producer
    time.sleep(5)

    # Close the Kafka producer
    producer.poll(0)


if __name__ == '__main__':
    main()