import requests
import unittest


class TestWeatherUtils(unittest.TestCase):

    response = None
    response_status_code = None
    request_root_url = 'http://localhost:8888/api'

    def test_apiweather_get(self):
        # Response with no query string
        self.response = requests.get(
            f'{self.request_root_url}/weather', timeout=15)
        self.response_status_code = self.response.status_code
        self.assertEqual(self.response_status_code, 200)

        # Response with complete query string
        self.response = requests.get(
            f'{self.request_root_url}/weather?page=1&station=USC00110072&date=20120101', timeout=15)
        self.response_status_code = self.response.status_code
        self.assertEqual(self.response_status_code, 200)

        # Response with incomplete query string
        self.response = requests.get(
            f'{self.request_root_url}/weather?page=1', timeout=15)
        self.response_status_code = self.response.status_code
        self.assertEqual(self.response_status_code, 200)
        self.response = requests.get(
            f'{self.request_root_url}/weather?station=USC00110072', timeout=15)
        self.response_status_code = self.response.status_code
        self.assertEqual(self.response_status_code, 200)
        self.response = requests.get(
            f'{self.request_root_url}/weather?date=20120101', timeout=15)
        self.response_status_code = self.response.status_code
        self.assertEqual(self.response_status_code, 200)
        self.response = requests.get(
            f'{self.request_root_url}/weather?page=1&station=USC00110072', timeout=15)
        self.response_status_code = self.response.status_code
        self.assertEqual(self.response_status_code, 200)
        self.response = requests.get(
            f'{self.request_root_url}/weather?station=USC00110072&date=20120101', timeout=15)
        self.response_status_code = self.response.status_code
        self.assertEqual(self.response_status_code, 200)
        self.response = requests.get(
            f'{self.request_root_url}/weather?page=1&date=20120101', timeout=15)
        self.response_status_code = self.response.status_code
        self.assertEqual(self.response_status_code, 200)

        # Other Response Codes
        self.response = requests.get(
            f'{self.request_root_url}/weather?page=0&station=USC00110072&date=20120101', timeout=15)
        self.response_status_code = self.response.status_code
        self.assertEqual(self.response_status_code, 404)
        self.response = requests.get(
            f'{self.request_root_url}/weather?page=1&station=USC001100&date=20120101', timeout=15)
        self.response_status_code = self.response.status_code
        self.assertEqual(self.response_status_code, 400)
        self.response = requests.get(
            f'{self.request_root_url}/weather?page=1&station=USC00110072&date=201201', timeout=15)
        self.response_status_code = self.response.status_code
        self.assertEqual(self.response_status_code, 400)
        self.response = requests.get(
            f'{self.request_root_url}/weather?page=1&station=USC12345678&date=20120101', timeout=15)
        self.response_status_code = self.response.status_code
        self.assertEqual(self.response_status_code, 404)
        self.response = requests.get(
            f'{self.request_root_url}/weather?page=1&station=USC00110072&date=20230101', timeout=15)
        self.response_status_code = self.response.status_code
        self.assertEqual(self.response_status_code, 404)

    def test_apiweatherstats_get(self):
        # Response with no query string
        self.response = requests.get(
            f'{self.request_root_url}/weather/stats', timeout=15)
        self.response_status_code = self.response.status_code
        self.assertEqual(self.response_status_code, 200)

        # Response with complete query string
        self.response = requests.get(
            f'{self.request_root_url}/weather/stats?page=1&station=USC00110072&year=2012', timeout=15)
        self.response_status_code = self.response.status_code
        self.assertEqual(self.response_status_code, 200)

        # Response with incomplete query string
        self.response = requests.get(
            f'{self.request_root_url}/weather/stats?page=1', timeout=15)
        self.response_status_code = self.response.status_code
        self.assertEqual(self.response_status_code, 200)
        self.response = requests.get(
            f'{self.request_root_url}/weather/stats?station=USC00110072', timeout=15)
        self.response_status_code = self.response.status_code
        self.assertEqual(self.response_status_code, 200)
        self.response = requests.get(
            f'{self.request_root_url}/weather/stats?year=2012', timeout=15)
        self.response_status_code = self.response.status_code
        self.assertEqual(self.response_status_code, 200)
        self.response = requests.get(
            f'{self.request_root_url}/weather/stats?page=1&station=USC00110072', timeout=15)
        self.response_status_code = self.response.status_code
        self.assertEqual(self.response_status_code, 200)
        self.response = requests.get(
            f'{self.request_root_url}/weather/stats?station=USC00110072&year=2012', timeout=15)
        self.response_status_code = self.response.status_code
        self.assertEqual(self.response_status_code, 200)
        self.response = requests.get(
            f'{self.request_root_url}/weather/stats?page=1&year=2012', timeout=15)
        self.response_status_code = self.response.status_code
        self.assertEqual(self.response_status_code, 200)

        # Other Response Codes
        self.response = requests.get(
            f'{self.request_root_url}/weather/stats?page=0&station=USC00110072&year=2012', timeout=15)
        self.response_status_code = self.response.status_code
        self.assertEqual(self.response_status_code, 404)
        self.response = requests.get(
            f'{self.request_root_url}/weather/stats?page=1&station=USC001100&year=2012', timeout=15)
        self.response_status_code = self.response.status_code
        self.assertEqual(self.response_status_code, 400)
        self.response = requests.get(
            f'{self.request_root_url}/weather/stats?page=1&station=USC00110072&year=201', timeout=15)
        self.response_status_code = self.response.status_code
        self.assertEqual(self.response_status_code, 400)
        self.response = requests.get(
            f'{self.request_root_url}/weather/stats?page=1&station=USC12345678&year=2012', timeout=15)
        self.response_status_code = self.response.status_code
        self.assertEqual(self.response_status_code, 404)
        self.response = requests.get(
            f'{self.request_root_url}/weather/stats?page=1&station=USC00110072&year=2023', timeout=15)
        self.response_status_code = self.response.status_code
        self.assertEqual(self.response_status_code, 404)


if __name__ == '__main__':

    unittest.main()
