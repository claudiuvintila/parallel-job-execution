import json
import os

from rabbitmq.consumer import Consumer
from parallel_executor.business import Business


class ParallelConsumer(Consumer):
    def __init__(self, exchange, queue='standard', routing_key='standard_key', host='localhost', username='guest', password='guest'):
        super().__init__(exchange, queue, routing_key, host, username, password)

        self.business = Business()

    def process_task(self, body):
        obj = json.loads(body)

        if obj['method'] == 'process_file':
            self.business.process_file(obj['file'])


if __name__ == "__main__":
    consumer = ParallelConsumer(
        os.environ['EXCHANGE'],
        host=os.environ['RABBITMQ_HOST'],
        username=os.environ['RABBITMQ_USERNAME'],
        password=os.environ['RABBITMQ_PASSWORD']
    )
    consumer.start()
