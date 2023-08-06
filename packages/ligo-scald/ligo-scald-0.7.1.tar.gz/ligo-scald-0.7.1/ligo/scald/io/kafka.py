#!/usr/bin/env python
from __future__ import absolute_import

__author__ = "Patrick Godwin (patrick.godwin@ligo.org)"
__description__ = "a module for kafka I/O utilities"

#-------------------------------------------------
### imports

from collections import defaultdict
import json
import logging

import numpy
from kafka import KafkaProducer, KafkaConsumer


#-------------------------------------------------
### classes

class Reporter(object):
    """Handles storing of metrics into Kafka.

    Parameters
    ----------
    hostname : `str`
        the hostname to connect to, defaults to localhost
    port : `int`
        the port to connect to, defaults to 8086

    """
    def __init__(self, hostname='localhost', port=8086, **kwargs):
        self.hostname = hostname
        self.port = port

        self.producer = KafkaProducer(
            bootstrap_servers=[':'.join([self.hostname, str(self.port)])],
            key_serializer=lambda m: json.dumps(m).encode('utf-8'),
            value_serializer=lambda m: json.dumps(m).encode('utf-8'),
        )

    def store(self, schema, data, tags=None):
        """Stores data into Kafka.

        Parameters
        ----------
        schema : `str`
            the schema name
        data : `dict`
            the data to store

        """
        if tags:
            if isinstance(tags, list):
                tags = '.'.join(tags)
            self.producer.send(schema, key=tags, value=data)
        else:
            self.producer.send(schema, value=data)


#-------------------------------------------------
### functions

def retrieve_timeseries(consumer, routes, timeout = 1000, max_records = 1000):
    """!
    A function to pull data from kafka for a set of jobs (topics) and
    routes (keys in the incoming json messages)
    """
    data = {route: defaultdict(lambda: {'time': [], 'fields': {'data': []}}) for route in routes}

    ### retrieve timeseries for all routes and topics
    msg_pack = consumer.poll(timeout_ms = timeout, max_records = max_records)
    for tp, messages in msg_pack.items():
        for message in messages:
            try:
                job = message.key
                route = message.topic
                data[route][job]['time'].extend(message.value['time'])
                data[route][job]['fields']['data'].extend(message.value['data'])
            except KeyError: ### no route in message
                pass

    ### convert series to numpy arrays
    for route in routes:
        for job in data[route].keys():
            data[route][job]['time'] = numpy.array(data[route][job]['time'])
            data[route][job]['fields']['data'] = numpy.array(data[route][job]['fields']['data'])

    return data


def retrieve_triggers(consumer, jobs, route_name = 'coinc', timeout = 1000, max_records = 1000):
    """!
    A function to pull triggers from kafka for a set of jobs (topics) and
    route_name (key in the incoming json messages)
    """
    triggers = []

    ### retrieve timeseries for all routes and topics
    msg_pack = consumer.poll(timeout_ms = timeout, max_records = max_records)
    for tp, messages in msg_pack.items():
        job = tp.topic
        if job not in jobs:
            continue
        for message in messages:
            try:
                triggers.extend(message.value[route_name])
            except KeyError: ### no route in message
                pass

    return triggers
