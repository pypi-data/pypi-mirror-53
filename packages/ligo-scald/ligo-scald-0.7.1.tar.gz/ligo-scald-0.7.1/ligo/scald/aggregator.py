#!/usr/bin/env python

__author__ = "Patrick Godwin (patrick.godwin@ligo.org)"
__description__ = "utilities to aggregate and store incoming metrics"

#-------------------------------------------------
### imports

import collections
import json
import logging
import os
import sys
import time
import timeit

import numpy
import yaml

from kafka import KafkaConsumer

from . import utils
from .io import influx, kafka


#-------------------------------------------------
### logging config

logger = logging.getLogger('kafka')
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)

#-------------------------------------------------
### aggregator utilities

def _add_parser_args(parser):
    parser.add_argument('-c', '--config',
                        help="sets dashboard/plot options based on yaml configuration. if not set, uses SCALDRC_PATH.")
    parser.add_argument('-b', '--backend', default='default',
                        help="chooses data backend to use from config. default = 'default'.")
    parser.add_argument('-d', '--data-type', default='timeseries',
                        help = "Sets the data type of metrics expected from [timeseries|triggers]. default = timeseries.")
    parser.add_argument('-n', '--hostname', default='localhost',
                        help="specify Kafka hostname to read metrics from. default = localhost.")
    parser.add_argument('-p', '--port', type=int, default=8086,
                        help="specify Kafka port to read metrics from. default = 8086")
    parser.add_argument('-s', '--schema', action='append',
                        help="Specify schema to use for aggregation. Can be given multiple times.")
    parser.add_argument('-t', '--tag', default='generic',
                        help = "Specify a tag for this aggregator job. default = 'generic'.")
    parser.add_argument('--across-jobs', action = 'store_true',
                        help = "If set, aggregate data across jobs as well.")
    parser.add_argument('--processing-cadence', default = 0.5,
                        help = "Rate at which the aggregator acquires and processes data. default = 0.5 seconds.")


#-------------------------------------------------
### main

def main(args=None):
    """Aggregates and stores metrics to a data backend

    """
    if not args:
        parser = argparse.ArgumentParser()
        _parser_add_arguments(parser)
        args = parser.parse_args()

    schemas = args.schema

    ### sanity checking
    assert args.data_type in ('timeseries', 'triggers'), '--data-type must be one of [timeseries|triggers]'

    if args.data_type == 'triggers':
        assert len(schemas) == 1, 'only one schema allowed if --data-type = triggers'

    ### load configuration
    config = None
    if args.config:
        config_path = args.config
    else:
        config_path = os.getenv('SCALDRC_PATH')
    if not config_path:
        raise KeyError('no configuration file found, please set your SCALDRC_PATH correctly or add --config param')
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # instantiate a consumer to subscribe to all of our topics, i.e., jobs
    consumer = KafkaConsumer(
        *schemas,
        bootstrap_servers=[':'.join([args.hostname, str(args.port)])],
        key_deserializer=lambda m: json.loads(m.decode('utf-8')),
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        group_id='aggregator_{}_{}'.format(args.tag, args.schema[0]),
        auto_offset_reset='latest',
        max_poll_interval_ms = 60000,
        session_timeout_ms=30000,
        heartbeat_interval_ms=10000,
        reconnect_backoff_ms=5000,
        reconnect_backoff_max_ms=30000
    )

    # set up aggregator
    aggregator_settings = config['backends'][args.backend]
    aggregator_settings['reduce_across_tags'] = args.across_jobs
    aggregator = influx.Aggregator(**aggregator_settings)

    # register measurement schemas for aggregators
    aggregator.load(path=config_path)

    # start an infinite loop to keep updating and aggregating data
    while True:
        logging.info("retrieving data from kafka")
        start = timeit.default_timer()

        if args.data_type == 'timeseries':
            data = kafka.retrieve_timeseries(consumer, schemas, max_records = 2000)
        elif args.data_type == 'triggers':
            data = kafka.retrieve_triggers(consumer, schemas, route_name = schemas[0], max_records = 2000)

        retrieve_elapsed = timeit.default_timer() - start
        logging.info("time to retrieve data: %.1f s" % retrieve_elapsed)

        # store and reduce data for each job
        start = timeit.default_timer()
        for schema in schemas:
            logging.info("storing and reducing metrics for schema: %s" % schema)
            if args.data_type == 'timeseries':
                aggregator.store_columns(schema, data[schema], aggregate=config['schemas'][schema]['aggregate'])
            elif args.data_type == 'triggers':
                far_key = config['schemas'][schema]['far_key']
                time_key = config['schemas'][schema]['time_key']
                aggregator.store_triggers(schema, [trg for trg in data if far_key in trg], far_key = far_key, time_key = time_key)

        store_elapsed = timeit.default_timer() - start
        logging.info("time to store/reduce %s: %.1f s" % (args.data_type, store_elapsed))

        time.sleep(max(args.processing_cadence - store_elapsed - retrieve_elapsed, args.processing_cadence))

    # close connection to consumer if using kafka
    if consumer:
        consumer.close()

    # always end on an error so that condor won't think we're done and will
    # restart us
    sys.exit(1)
