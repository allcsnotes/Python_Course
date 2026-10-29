import os

import redis
from confluent_kafka import Consumer, Producer, TopicPartition

r = redis.from_url(os.environ["REDIS_URL"], decode_responses=True)
KAFKA = os.environ["KAFKA_SERVERS"]


def topic_size(topic):
    c = Consumer({"bootstrap.servers": KAFKA, "group.id": "size-check"})
    low, high = c.get_watermark_offsets(TopicPartition(topic, 0), timeout=10)
    c.close()
    return high - low
