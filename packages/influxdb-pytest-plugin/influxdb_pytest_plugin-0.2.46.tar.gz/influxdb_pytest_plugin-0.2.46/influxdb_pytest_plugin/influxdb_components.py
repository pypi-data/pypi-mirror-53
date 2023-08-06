from influxdb import InfluxDBClient


class Influxdb_Components():
    _client = None

    def __init__(self, host, port, db_user, db_password, db_name):
        self._client = InfluxDBClient(host, port, db_user, db_password, db_name)

    def get_client(self):
        return self._client