from influxdb_client import InfluxDBClient
from data_connector.base_connector import BaseConnector
import os

class TemperatureConnector(BaseConnector):
    def __init__(self, name="debo_temp_1", bucket="sensordata"):
        super().__init__(name, bucket)
        self.client = InfluxDBClient(
            url=os.getenv("INFLUX_URL"),
            token=os.getenv("INFLUX_TOKEN"),
            org=os.getenv("INFLUX_ORG")
        )

    def read(self):
        query = f'''
        from(bucket: "{self.bucket}")
          |> range(start: -1h)
          |> filter(fn: (r) => r._measurement == "temperature")
          |> filter(fn: (r) => r.sensor == "{self.name}")
          |> last()
        '''
        result = self.client.query_api().query(query)
        for table in result:
            for record in table.records:
                return round(record.get_value(), 2)
        return None
