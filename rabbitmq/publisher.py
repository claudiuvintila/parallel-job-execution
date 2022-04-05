# -*- coding: utf-8 -*-
# pylint: disable=C0111,C0103,R0205

import os
import logging
import pika
from pika.exchange_type import ExchangeType
from pika.spec import TRANSIENT_DELIVERY_MODE

logging.basicConfig(level=logging.INFO)


class Publisher:
    def __init__(self, exchange, exchange_type=ExchangeType.direct, host='localhost', username='guest', password='guest'):
        self.host = host
        self.exchange = exchange
        self.exchange_type = exchange_type
        credentials = pika.PlainCredentials(username, password)
        parameters = pika.ConnectionParameters(host, credentials=credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange,
             exchange_type=self.exchange_type,
             passive=False,
             durable=True,
             auto_delete=False)

    def __del__(self):
        self.connection.close()

    def publish(self, msg, routing_key='standard_key'):

        print("Sending message to create a queue")
        self.channel.basic_publish(
            self.exchange, routing_key, msg,
            pika.BasicProperties(content_type='text/plain',
                                 delivery_mode=TRANSIENT_DELIVERY_MODE))


if __name__ == "__main__":
    publisher = Publisher(
        os.environ['EXCHANGE'],
        host=os.environ['RABBITMQ_HOST'],
        username=os.environ['RABBITMQ_USERNAME'],
        password=os.environ['RABBITMQ_PASSWORD']
    )
    publisher.publish('test msg')


