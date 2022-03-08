from bridge import Bridge
import http.client
import json



class Adapter:

    def __init__(self, input):
        self.id = input.get('id', '1')
        self.request_data = input.get('data')
        if self.validate_request_data():
            self.bridge = Bridge()
            self.set_params()
            self.create_request()
        else:
            self.result_error('No data provided')

    def validate_request_data(self):
        if self.request_data is None:
            return False
        if self.request_data == {}:
            return False
        return True

    def set_params(self):
        self.station_id = self.request_data.get("station_id")

    def create_request(self):
        try:
            conn = http.client.HTTPSConnection("live-stock-market.p.rapidapi.com")

            headers = {
                'x-rapidapi-host': "live-stock-market.p.rapidapi.com",
                'x-rapidapi-key': "<YOUR API KEY>"
            }

            conn.request("GET", "/yahoo-finance/v1/quote?symbols={}".format(self.station_id), headers=headers)

            res = conn.getresponse()
            data = res.read()

            response = data.decode("utf-8")

            data = json.loads(response)

            # parse response data
            self.result = data["data"]

            data['result'] = self.result
            self.result_success(data)
        except Exception as e:
            self.result_error(e)
        finally:
            self.bridge.close()

    def result_success(self, data):
        self.result = {
            'jobRunID': self.id,
            'data': data,
            'result': self.result,
            'statusCode': 200,
        }

    def result_error(self, error):
        self.result = {
            'jobRunID': self.id,
            'status': 'errored',
            'error': f'There was an error: {error}',
            'statusCode': 500,
        }
