influxdb-client-python
======================

.. marker-index-start

.. image:: https://circleci.com/gh/influxdata/influxdb-client-python.svg?style=svg
   :target: https://circleci.com/gh/influxdata/influxdb-client-python
   :alt: CircleCI


.. image:: https://codecov.io/gh/influxdata/influxdb-client-python/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/influxdata/influxdb-client-python
   :alt: codecov

.. image:: https://img.shields.io/circleci/project/github/influxdata/influxdb-client-python/master.svg
   :target: https://circleci.com/gh/influxdata/influxdb-client-python
   :alt: CI status

.. image:: https://img.shields.io/codecov/c/github/influxdata/influxdb-client-python.svg
   :target: https://codecov.io/gh/influxdata/influxdb-client-python
   :alt: Coverage

.. image:: https://img.shields.io/pypi/v/influxdb-client-python.svg
   :target: https://pypi.python.org/pypi/influxdb-client-python
   :alt: PyPI package

.. image:: https://img.shields.io/pypi/pyversions/influxdb-client-python.svg
   :target: https://pypi.python.org/pypi/influxdb-client-python
   :alt: Supported Python versions

.. image:: https://readthedocs.org/projects/influxdb-client/badge/?version=latest
   :target: https://influxdb-client.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation status

.. _documentation: https://influxdb-client.readthedocs.io

InfluxDB 2.0 python client library. The library covers InfluxDB 2.0

InfluxDB 2.0 client features
----------------------------

- Querying data
    - using the Flux language
    - into csv, raw data, `flux_table <https://github.com/influxdata/influxdb-client-python/blob/master/influxdb_client/client/flux_table.py#L5>`_ structure
- Writing data using
    - `Line Protocol <https://docs.influxdata.com/influxdb/v1.6/write_protocols/line_protocol_tutorial>`_
    - `Data Point <https://github.com/influxdata/influxdb-client-python/blob/master/influxdb_client/client/write/point.py#L16>`__
    - `RxPY`_ Observable
    - Not implemented yet
      - write user types using decorator
      - write Pandas DataFrame
- `InfluxDB 2.0 API <https://github.com/influxdata/influxdb/blob/master/http/swagger.yml>`_ client for management
    - the client is generated from the `swagger <https://github.com/influxdata/influxdb/blob/master/http/swagger.yml>`_ by using the `openapi-generator <https://github.com/OpenAPITools/openapi-generator>`_
    - organizations & users management
    - buckets management
    - tasks management
    - authorizations
    - health check

Installation
------------
.. marker-install-start

InfluxDB python library uses `RxPY <https://github.com/ReactiveX/RxPY>`_ - The Reactive Extensions for Python (RxPY).

**Python 3.6** or later is required.


pip install
^^^^^^^^^^^

The python package is hosted on Github, you can install latest version directly:

.. code-block:: sh

   pip3 install git+https://github.com/influxdata/influxdb-client-python.git

Then import the package:

.. code-block:: python

   import influxdb_client

Setuptools
^^^^^^^^^^

Install via `Setuptools <http://pypi.python.org/pypi/setuptools>`_.

.. code-block:: sh

   python setup.py install --user

(or ``sudo python setup.py install`` to install the package for all users)

.. marker-install-end

Getting Started
---------------

Please follow the `Installation`_ and then run the following:

.. marker-query-start

.. code-block:: python

   from influxdb_client import InfluxDBClient, Point
   from influxdb_client.client.write_api import SYNCHRONOUS

   bucket = "my-bucket"

   client = InfluxDBClient(url="http://localhost:9999", token="my-token", org="my-org")

   write_api = client.write_api(write_options=SYNCHRONOUS)
   query_api = client.query_api()

   p = Point("my_measurement").tag("location", "Prague").field("temperature", 25.3)

   write_api.write(bucket=bucket, org="my-org", record=p)

   ## using Table structure
   tables = query_api.query('from(bucket:"my-bucket") |> range(start: -10m)')

   for table in tables:
       print(table)
       for row in table.records:
           print (row.values)


   ## using csv library
   csv_result = query_api.query_csv('from(bucket:"my-bucket") |> range(start: -10m)')
   val_count = 0
   for row in csv_result:
       for cell in row:
           val_count += 1

.. marker-query-end
.. marker-index-end


How to use
----------

Writes
^^^^^^
.. marker-writes-start

The `WriteApi <https://github.com/influxdata/influxdb-client-python/blob/master/influxdb_client/client/write_api.py>`_ supports synchronous, asynchronous and batching writes into InfluxDB 2.0.
The data should be passed as a `InfluxDB Line Protocol <https://docs.influxdata.com/influxdb/v1.6/write_protocols/line_protocol_tutorial/>`_\ , `Data Point <https://github.com/influxdata/influxdb-client-python/blob/master/influxdb_client/client/write/point.py>`_ or Observable stream.

*The default instance of ``WriteApi`` use batching.*

Batching
""""""""

.. marker-batching-start

The batching is configurable by ``write_options``\ :

.. list-table::
   :header-rows: 1

   * - Property
     - Description
     - Default Value
   * - **batch_size**
     - the number of data pointx to collect in a batch
     - ``1000``
   * - **flush_interval**
     - the number of milliseconds before the batch is written
     - ``1000``
   * - **jitter_interval**
     - the number of milliseconds to increase the batch flush interval by a random amount
     - ``0``
   * - **retry_interval**
     - the number of milliseconds to retry unsuccessful write. The retry interval is used when the InfluxDB server does not specify "Retry-After" header.
     - ``1000``


.. code-block:: python

   import rx
   from rx import operators as ops

   from influxdb_client import InfluxDBClient, Point, WriteOptions
   from influxdb_client.client.write_api import SYNCHRONOUS

   _client = InfluxDBClient(url="http://localhost:9999", token="my-token", org="my-org")
   _write_client = _client.write_api(write_options=WriteOptions(batch_size=500, 
                                                                flush_interval=10_000, 
                                                                jitter_interval=2_000, 
                                                                retry_interval=5_000))

   """
   Write Line Protocol
   """
   _write_client.write("my-bucket", "my-org", "h2o_feet,location=coyote_creek water_level=1.0 1")
   _write_client.write("my-bucket", "my-org", ["h2o_feet,location=coyote_creek water_level=2.0 2",
                                               "h2o_feet,location=coyote_creek water_level=3.0 3"])

   """
   Write Data Point
   """
   _write_client.write("my-bucket", "my-org", Point("h2o_feet").tag("location", "coyote_creek").field("water_level", 4.0).time(4))
   _write_client.write("my-bucket", "my-org", [Point("h2o_feet").tag("location", "coyote_creek").field("water_level", 5.0).time(5),
                                               Point("h2o_feet").tag("location", "coyote_creek").field("water_level", 6.0).time(6)])

   """
   Write Observable stream
   """
   _data = rx \
       .range(7, 11) \
       .pipe(ops.map(lambda i: "h2o_feet,location=coyote_creek water_level={0}.0 {0}".format(i)))

   _write_client.write("my-bucket", "my-org", _data)


   """
   Close client
   """
   _write_client.__del__()
   _client.__del__()

.. marker-batching-end

Asynchronous client
"""""""""""""""""""

Data are writes in an asynchronous HTTP request.

.. code-block:: python

   from influxdb_client  import InfluxDBClient
   from influxdb_client.client.write_api import ASYNCHRONOUS

   client = InfluxDBClient(url="http://localhost:9999", token="my-token", org="my-org")
   write_client = client.write_api(write_options=ASYNCHRONOUS)

   ...

   client.__del__()

Synchronous client
""""""""""""""""""

Data are writes in a synchronous HTTP request.

.. code-block:: python

   from influxdb_client  import InfluxDBClient
   from influxdb_client .client.write_api import SYNCHRONOUS

   client = InfluxDBClient(url="http://localhost:9999", token="my-token", org="my-org")
   write_client = client.write_api(write_options=SYNCHRONOUS)

   ...

   client.__del__()

How to efficiently import large dataset
"""""""""""""""""""""""""""""""""""""""


* sources - `import_data_set.py <https://github.com/influxdata/influxdb-client-python/blob/master/tests/import_data_set.py>`_

.. code-block:: python

   """
   Import VIX - CBOE Volatility Index - from "vix-daily.csv" file into InfluxDB 2.0

   https://datahub.io/core/finance-vix#data
   """

   from collections import OrderedDict
   from csv import DictReader
   from datetime import datetime

   import rx
   from rx import operators as ops

   from influxdb_client import InfluxDBClient, Point, WriteOptions

   def parse_row(row: OrderedDict):
       """Parse row of CSV file into Point with structure:

           financial-analysis,type=ily close=18.47,high=19.82,low=18.28,open=19.82 1198195200000000000

       CSV format:
           Date,VIX Open,VIX High,VIX Low,VIX Close\n
           2004-01-02,17.96,18.68,17.54,18.22\n
           2004-01-05,18.45,18.49,17.44,17.49\n
           2004-01-06,17.66,17.67,16.19,16.73\n
           2004-01-07,16.72,16.75,15.5,15.5\n
           2004-01-08,15.42,15.68,15.32,15.61\n
           2004-01-09,16.15,16.88,15.57,16.75\n
           ...

       :param row: the row of CSV file
       :return: Parsed csv row to [Point]
       """
       return Point("financial-analysis") \
           .tag("type", "vix-daily") \
           .field("open", float(row['VIX Open'])) \
           .field("high", float(row['VIX High'])) \
           .field("low", float(row['VIX Low'])) \
           .field("close", float(row['VIX Close'])) \
           .time(datetime.strptime(row['Date'], '%Y-%m-%d'))


   """
   Converts vix-daily.csv into sequence of datad point
   """
   data = rx \
       .from_iterable(DictReader(open('vix-daily.csv', 'r'))) \
       .pipe(ops.map(lambda row: parse_row(row)))

   client = InfluxDBClient(url="http://localhost:9999", token="my-token", org="my-org", debug=True)

   """
   Create client that writes data in batches with 500 items.
   """
   write_api = client.write_api(write_options=WriteOptions(batch_size=500, jitter_interval=1_000))

   """
   Write data into InfluxDB
   """
   write_api.write(org="my-org", bucket="my-bucket", record=data)
   write_api.__del__()

   """
   Querying max value of CBOE Volatility Index
   """
   query = 'from(bucket:"my-bucket")' \
           ' |> range(start: 0, stop: now())' \
           ' |> filter(fn: (r) => r._measurement == "financial-analysis")' \
           ' |> max()'
   result = client.query_api().query(org="my-org", query=query)

   """
   Processing results
   """
   print()
   print("=== results ===")
   print()
   for table in result:
       for record in table.records:
           print('max {0:5} = {1}'.format(record.get_field(), record.get_value()))

   """
   Close client
   """
   client.__del__()

.. marker-writes-end


Efficiency write data from IOT sensor
"""""""""""""""""""""""""""""""""""""
.. marker-iot-start

* sources - `iot_sensor.py <https://github.com/influxdata/influxdb-client-python/blob/master/tests/iot_sensor.py>`_

.. code-block:: python

   """
   Efficiency write data from IOT sensor - write changed temperature every minute
   """
   import atexit
   import platform
   from datetime import timedelta

   import psutil as psutil
   import rx
   from rx import operators as ops

   from influxdb_client import InfluxDBClient, WriteApi, WriteOptions

   def on_exit(db_client: InfluxDBClient, write_api: WriteApi):
       """Close clients after terminate a script.

       :param db_client: InfluxDB client
       :param write_api: WriteApi
       :return: nothing
       """
       write_api.__del__()
       db_client.__del__()


   def sensor_temperature():
       """Read a CPU temperature. The [psutil] doesn't support MacOS so we use [sysctl].

       :return: actual CPU temperature
       """
       os_name = platform.system()
       if os_name == 'Darwin':
           from subprocess import check_output
           output = check_output(["sysctl", "machdep.xcpm.cpu_thermal_level"])
           import re
           return re.findall(r'\d+', str(output))[0]
       else:
           return psutil.sensors_temperatures()["coretemp"][0]


   def line_protocol(temperature):
       """Create a InfluxDB line protocol with structure:

           iot_sensor,hostname=mine_sensor_12,type=temperature value=68

       :param temperature: the sensor temperature
       :return: Line protocol to write into InfluxDB
       """

       import socket
       return 'iot_sensor,hostname={},type=temperature value={}'.format(socket.gethostname(), temperature)


   """
   Read temperature every minute; distinct_until_changed - produce only if temperature change
   """
   data = rx\
       .interval(period=timedelta(seconds=60))\
       .pipe(ops.map(lambda t: sensor_temperature()),
             ops.distinct_until_changed(),
             ops.map(lambda temperature: line_protocol(temperature)))

   _db_client = InfluxDBClient(url="http://localhost:9999", token="my-token", org="my-org", debug=True)

   """
   Create client that writes data into InfluxDB
   """
   _write_api = _db_client.write_api(write_options=WriteOptions(batch_size=1))
   _write_api.write(org="my-org", bucket="my-bucket", record=data)


   """
   Call after terminate a script
   """
   atexit.register(on_exit, _db_client, _write_api)

   input()

.. marker-iot-end

Advanced Usage
--------------

Gzip support
^^^^^^^^^^^^
.. marker-gzip-start

``InfluxDBClient`` does not enable gzip compression for http requests by default. If you want to enable gzip to reduce transfer data's size, you can call:

.. code-block:: python

   from influxdb_client import InfluxDBClient

   _db_client = InfluxDBClient(url="http://localhost:9999", token="my-token", org="my-org", enable_gzip=True)

.. marker-gzip-end