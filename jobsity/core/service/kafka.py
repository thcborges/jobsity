import json
from functools import wraps

from decouple import config
from kafka import KafkaConsumer, KafkaProducer
from kafka.consumer.fetcher import ConsumerRecord

BOOTSTRAP_SERVERS = config('BOOTSTRAP_SERVERS')


def message_decode(message: ConsumerRecord) -> dict[any]:
    return json.loads(message.value)


def kafka_consumer(topic, **kafka_kwargs):
    def decorator_kafka_consumer(func):
        @wraps(func)
        def wrapper_kafka_consumer(*args, **kwargs):
            try:
                while True:
                    messages = KafkaConsumer(
                        topic,
                        bootstrap_servers=BOOTSTRAP_SERVERS,
                        **kafka_kwargs
                    )
                    for message in messages:
                        func(message_decode(message), *args, **kwargs)
            except KeyboardInterrupt:
                print('Finishing...')

        return wrapper_kafka_consumer

    return decorator_kafka_consumer


def get_producer() -> KafkaProducer:
    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('UTF-8'),
    )
    return producer
