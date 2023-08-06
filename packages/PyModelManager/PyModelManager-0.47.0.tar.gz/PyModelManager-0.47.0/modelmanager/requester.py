import json
import requests
from io import IOBase


class Requester(object):
    def __init__(self, base_url=None, login=None, password=None) -> None:
        super().__init__()

        self._base_url = base_url
        self._login = login
        self._password = password

    def __make_absolute_url(self, url):
        return self._base_url + url

    def request_json(self, verb, url, parameters=None, headers=None, input=None):
        def encode(input):
            return "application/json", json.dumps(input)

        res = self.__request(verb, url, parameters, headers, input, encode, None)

        return res.status_code, res.text

    def request_blob(self, verb, url, parameters=None, headers=None):
        res = self.__request(verb, url, parameters, headers, None, None, None)

        return res.status_code, res.content

    def request_files(self, verb, url, parameters=None, headers=None, files=None):
        name, file = files

        res = self.__request(verb, url, parameters, headers, None, None, {name: (file)})

        if file and isinstance(file, IOBase):
            file.close()

        return res.status_code, res.text

    def request_json_and_check(self, verb, url, parameters=None, headers=None, input=None):
        status, data = self.request_json(verb, url, parameters, headers, input)
        if status >= 400:
            raise Exception('{} {} {} {}'.format(verb, url, status, data))
        return status, self.__structured_from_json(data)

    def request_files_and_check(self, verb, url, files, parameters=None, headers=None):
        status, data = self.request_files(verb, url, parameters, headers, files)
        if status >= 400:
            raise Exception('{} {} {} {}'.format(verb, url, status, data))
        return status, self.__structured_from_json(data)

    def request_blob_and_check(self, verb, url, parameters=None, headers=None):
        status, data = self.request_blob(verb, url, parameters, headers)
        if status >= 400:
            raise Exception('{} {} {} {}'.format(verb, url, status, data))
        return status, self.__structured_from_json(data)

    def __structured_from_json(self, data):
        if len(data) == 0:
            return None
        else:
            if isinstance(data, bytes):
                data = data.decode("utf-8")
            try:
                return json.loads(data)
            except ValueError:
                return {'data': data}

    def __request(self, verb, url, parameters, headers, input, encode, files):
        if not verb in ["GET", "HEAD", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]:
            raise Exception("Bad http method name '%s'" % verb)
        absolute_url = self.__make_absolute_url(url)

        if parameters is None:
            parameters = dict()
        if headers is None:
            headers = dict()

        encoded_input = None
        if input:
            headers['Content-Type'], encoded_input = encode(input)

        res = requests.request(
            method=verb,
            url=absolute_url,
            params=parameters,
            headers=headers,
            data=encoded_input,
            files=files
        )

        return res
