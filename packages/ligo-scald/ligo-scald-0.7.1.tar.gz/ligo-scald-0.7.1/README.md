![ligo-scald](https://git.ligo.org/gstlal-visualisation/ligo-scald/raw/master/doc/_static/logo.png "ligo-scald")

SCalable Analytics for LIGO/Virgo/Kagra Data
==========================================================================

[![pipeline status](https://git.ligo.org/gstlal-visualisation/ligo-scald/badges/master/pipeline.svg)](https://git.ligo.org/gstlal-visualisation/ligo-scald/commits/master)
[![coverage report](https://git.ligo.org/gstlal-visualisation/ligo-scald/badges/master/coverage.svg)](https://git.ligo.org/gstlal-visualisation/ligo-scald/commits/master)
[![conda-forge](https://img.shields.io/conda/vn/conda-forge/ligo-scald.svg)](https://anaconda.org/conda-forge/ligo-scald)

|              |        |
| ------------ | ------ |
| **Version:** | 0.6.0  |
| **Web:**     | https://docs.ligo.org/gstlal-visualisation/ligo-scald  |
| **Source:**  | http://software.ligo.org/lscsoft/source/ligo-scald-0.6.0.tar.gz  |


**ligo-scald** is a dynamic data visualization and monitoring tool for gravitational-wave data.

## Features:

* Provides a web-based dashboard for visualizing/exploring realtime and historical data.
* Streaming timeseries, heatmap and 'latest' visualizations.
* Utilities for storing and aggregating timeseries data that is accessible via HTTP API.
* Set up nagios monitoring based on thresholds or job heartbeats.
* Full integration with InfluxDB, a timeseries database, as a data backend.
* A mock database to serve fake data for testing purposes.

**ligo-scald** also provides a command line interface for various tasks:

* `scald serve`: serving data and dynamic html pages
* `scald deploy`: deploys a web application on the LDG
* `scald mock`: starts up a mock database that generates data based on HTTP requests
* `scald report`: generates offline html reports

## CLI usage:

Serve data locally:

```
scald serve -c /path/to/config.yml
```

Mock a database to serve HTTP requests and return fake data:

```
scald mock
```

Deploy a CGI-based web application on the Ligo Data Grid to serve the dashboard and data requests:

```
scald deploy -c /path/to/config.yml -o /path/to/public_html -n web_application_name
```

A full list of commands can be viewed with:

```
scald --help
```

A list of all command-line options can be displayed for any command:

```
scald serve --help
```

## Storing data into InfluxDB using Aggregator classes:

```python
from ligo.scald import io

### instantiate the aggregator
aggregator = io.influx.Aggregator(hostname='influx.hostname', port=8086, db='your_database')

### register a measurement schema (how data is stored in backend)
measurement = 'my_meas'
columns = ('column1', 'column2')
column_key = 'column1'
tags = ('tag1', 'tag2')
tag_key = 'tag2'

aggregator.register_schema(measurement, columns, column_key, tags, tag_key)

### store and aggregate data

### option 1: store data in row form
row_1 = {'time': 1234567890, 'fields': {'column1': 1.2, 'column2': 0.3}}
row_2 = {'time': 1234567890.5, 'fields': {'column1': 0.3, 'column2': 0.4}}

row_3 = {'time': 1234567890, 'fields': {'column1': 2.3, 'column2': 1.1}}
row_4 = {'time': 1234567890.5, 'fields': {'column1': 0.1, 'column2': 2.3}}

rows = {('001', 'andrew'): [row_1, row_2], ('002', 'parce'): [row_3, row_4]}

aggregator.store_rows(measurement, rows)

### option 2: store data in column form
cols_1 = {
    'time': [1234567890, 1234567890.5],
    'fields': {'column1': [1.2, 0.3], 'column2': [0.3, 0.4]}
}
cols_2 = {
    'time': [1234567890, 1234567890.5],
    'fields': {'column1': [2.3, 0.1], 'column2': [1.1, 2.3]}
}
cols = {('001', 'andrew'): cols_1, ('002', 'parce'): cols_2}

aggregator.store_columns(measurement, cols)

```

## Installation:

1. Conda installation:

```
conda install -c conda-forge ligo-scald
```

2. Source installation:

First, install all the dependencies listed below. Then install using setup.py:

```
python setup.py install --prefix=path/to/install/dir
```

Make sure to update your PYTHONPATH to point to the install directory.

Alternatively, you could install ligo-scald with conda if you have all your dependencies installed from conda-forge:

```
pip install .
```

## Quick Start

In two separate terminals execute first

```
scald mock
```

Then

```
scald serve -c /path/to/example_config.yml
```

With the above two processes running, you should be able to navigate to the following address in your web browser localhost:8080

## Dependencies:

  * bottle
  * h5py
  * ligo-common
  * numpy
  * python-dateutil
  * pyyaml
  * urllib3
