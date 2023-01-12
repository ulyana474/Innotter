import json
import os
import pika
from pika.exchange_type import ExchangeType

connection = None

def publish(message : dict):
    credentials = pika.PlainCredentials('guest', 'guest')
    HOST = "localhost"
    if os.getenv("TEST", 0) == 0:
        HOST = os.getenv('RABBIT_MQ_HOST', "localhost")
    parameters = pika.ConnectionParameters(HOST,
                                        os.environ.get('RABBIT_MQ_PORT', ''),
                                        '/',
                                        credentials)
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()
    
    channel.exchange_declare(
        exchange='test_exchange',
        exchange_type=ExchangeType.direct,
        passive=False,
        durable=True,
        auto_delete=False)
    channel.queue_declare(queue='standard', auto_delete=True)
    channel.queue_bind(
        queue='standard', exchange='test_exchange', routing_key='standard_key')

    channel.basic_publish(exchange='test_exchange', routing_key='standard_key', body=json.dumps(message))
    print(" [x] Sent")
    connection.close()
