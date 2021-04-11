import os
from stats import Stats
from time import sleep

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

influx_url = os.getenv('OMNI_INFLUX_URL')
influx_token = os.getenv('OMNI_INFLUX_TOKEN')
influx_bucket = os.getenv('OMNI_INFLUX_BUCKET')
influx_org = os.getenv('OMNI_INFLUX_ORG')


client = InfluxDBClient(url=influx_url, token=influx_token)
write_api = client.write_api(write_options=SYNCHRONOUS)
data_rate = int(os.getenv('OMNI_DATA_RATE_SECONDS', 5))
stats = Stats()

while True:
    print('Sending data...')
    data = stats.get_all(influx_format=True)
    write_api.write(influx_bucket, influx_org, data)
    sleep(data_rate)
