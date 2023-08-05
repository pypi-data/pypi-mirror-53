import requests
import json

__version__ = '0.0.1'


class ApiClient(object):

    def __init__(self, url, version='api'):
        self.waves_url = url
        self.api_version = version
        self.session = requests.Session()
        # self.token = self.login(username, password)

    def register_businesstask(self):
        url = self._build_url('business-tasks')
        response = requests.get(url, headers=self._get_headers())
        response = requests.post(url, data=json.dumps({
            'name': 'x',
        }), headers=self._get_headers())
        return response.json()

    def _get_headers(self, content_type='application/json'):
        headers = {
            'User-Agent': 'wavescli/{}'.format(__version__),
            'Content-Type': content_type
        }
        # token = getattr(self, 'token', None)
        # if token:
        #     headers['Authorization'] = token
        return headers

    def _build_url(self, endpoint):
        return '/'.join([self.waves_url, self.api_version, endpoint])


class ApiError(RuntimeError):

    def __init__(self, response):
        message = 'status={} data={}'.format(
            response.status_code, response.json())
        super(ApiError, self).__init__(message)
