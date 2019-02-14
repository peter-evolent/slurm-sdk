"""HTTPClient"""
import requests

from slurmsdk.exceptions import SDKException


class HTTPClient:
    def make_request(self, method: str, url: str,
                     data: dict = None, headers: dict = None, params: dict = None) -> dict:
        """Makes a HTTP request

        Args:
            method: HTTP method
            url: request url
            data: the body to attach to the request
            headers: dictionary of HTTP headers
            params: dictionary of query params

        Returns:
            data: the json-encoded content of a response

        Raises:
            SDKException:
                - connection error
                - invalid response content-type header
                - invalid response body (non-json)
        """
        try:
            resp = requests.request(
                method=method,
                url=url,
                json=data,
                headers=headers,
                params=params
            )
        except requests.exceptions.ConnectionError as e:
            raise SDKException(str(e))

        content_type = resp.headers['content-type']
        if content_type != 'application/json':
            raise SDKException(f'Invalid Content-Type: {content_type}')

        try:
            data = resp.json()
        except ValueError as e:
            raise SDKException(f'Invalid JSON response: {str(e)}')

        if not resp.ok:
            raise SDKException(resp.status_code, data=data)

        return data

    def get(self, url: str, headers: dict = None, params: dict = None):
        """Make a HTTP GET Request

        Args:
            url: request url
            headers: dictionary of HTTP headers
            params: dictionary of query params

        Returns:
            data: the json-encoded content of a response

        Raises:
            SDKException:
                - connection error
                - invalid response content-type header
                - invalid response body (non-json)
        """
        return self.make_request('GET', url, headers=headers, params=params)

    def post(self, url: str, data: dict = None, headers: dict = None):
        """Makes a HTTP POST request

        Args:
            url: request url
            data: the body to attach to the request
            headers: dictionary of HTTP headers

        Returns:
            data: the json-encoded content of a response

        Raises:
            SDKException:
                - connection error
                - invalid response content-type header
                - invalid response body (non-json)
        """
        return self.make_request('POST', url, data=data, headers=headers)

    def put(self, url: str, data: dict = None, headers: dict = None):
        """Makes a HTTP PUT request

        Args:
            url: request url
            data: the body to attach to the request
            headers: dictionary of HTTP headers

        Returns:
            data: the json-encoded content of a response

        Raises:
            SDKException:
                - connection error
                - invalid response content-type header
                - invalid response body (non-json)
        """
        return self.make_request('PUT', url, data=data, headers=headers)

    def delete(self, url: str, headers: dict = None):
        """Makes a HTTP DELETE request

        Args:
            url: request url
            headers: dictionary of HTTP headers

        Returns:
            data: the json-encoded content of a response

        Raises:
            SDKException:
                - connection error
                - invalid response content-type header
                - invalid response body (non-json)
        """
        return self.make_request('DELETE', url, headers=headers)
