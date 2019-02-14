import json
from unittest.mock import Mock

import pytest
import responses

from slurmsdk.client import HTTPClient
from slurmsdk.exceptions import SDKException


@pytest.fixture
def resp_mock():
    with responses.RequestsMock() as resp:
        yield resp


@pytest.fixture
def make_request_mock(monkeypatch):
    mock = Mock()
    monkeypatch.setattr(HTTPClient, 'make_request', mock)
    return mock


def test_valid_json_response(resp_mock):
    url = 'http://my.test.com'
    resp_data = {'key': 'value'}
    resp_mock.add('GET', url, status=200,
                  content_type='application/json', json=resp_data)

    client = HTTPClient()
    resp = client.make_request('GET', url)

    assert resp == resp_data


def test_valid_json_error_response(resp_mock):
    url = 'http://my.test.com'
    resp_data = {'key': 'value'}
    resp_mock.add('GET', url, status=400,
                  content_type='application/json', json=resp_data)

    client = HTTPClient()
    with pytest.raises(SDKException) as exc:
        client.make_request('GET', url)

    assert exc.value.message == 400
    assert exc.value.data == resp_data


def test_connection_error(resp_mock):
    url = 'http://my.test.com'

    client = HTTPClient()
    with pytest.raises(SDKException) as exc:
        client.make_request('GET', url)

    assert url in exc.value.message


def test_invalid_response_content_type(resp_mock):
    url = 'http://my.test.com'
    resp_mock.add('GET', url, status=200, content_type='plain/text')

    client = HTTPClient()
    with pytest.raises(SDKException) as exc:
        client.make_request('GET', url)

    assert exc.value.message == 'Invalid Content-Type: plain/text'


def test_non_json_response(resp_mock):
    url = 'http://my.test.com'
    text = 'response body'
    resp_mock.add('GET', url, status=200, content_type='application/json', body=text)

    client = HTTPClient()
    with pytest.raises(SDKException) as exc:
        client.make_request('GET', url)

    assert 'Invalid JSON response' in exc.value.message


def test_args_data(resp_mock):
    url = 'http://my.test.com'
    data = {'header': 'value'}
    resp_mock.add('GET', url, content_type='application/json', json={})

    client = HTTPClient()
    client.make_request('GET', url, data=data)

    assert json.loads(resp_mock.calls[0].request.body) == data


def test_args_headers(resp_mock):
    url = 'http://my.test.com'
    headers = {'header': 'value'}
    resp_mock.add('GET', url, content_type='application/json', json={})

    client = HTTPClient()
    client.make_request('GET', url, headers=headers)

    assert resp_mock.calls[0].request.headers.items() >= headers.items()


def test_args_params(resp_mock):
    url = 'http://my.test.com'
    params = {'param': 'value'}
    resp_mock.add('GET', url, content_type='application/json', json={})

    client = HTTPClient()
    client.make_request('GET', url, params=params)

    assert resp_mock.calls[0].request.url.endswith('?param=value')


def test_get(make_request_mock):
    headers = {'header': 'value'}
    params = {'param': 'value'}

    client = HTTPClient()
    client.get('http://my.test.com', headers=headers, params=params)

    make_request_mock.assert_called_once_with(
        'GET',
        'http://my.test.com',
        headers=headers,
        params=params
    )


def test_post(make_request_mock):
    data = {'key': 'value'}
    headers = {'header': 'value'}

    client = HTTPClient()
    client.post('http://my.test.com', data=data, headers=headers)

    make_request_mock.assert_called_once_with(
        'POST',
        'http://my.test.com',
        data=data,
        headers=headers
    )


def test_put(make_request_mock):
    data = {'key': 'value'}
    headers = {'header': 'value'}

    client = HTTPClient()
    client.put('http://my.test.com', data=data, headers=headers)

    make_request_mock.assert_called_once_with(
        'PUT',
        'http://my.test.com',
        data=data,
        headers=headers
    )


def test_delete(make_request_mock):
    headers = {'header': 'value'}

    client = HTTPClient()
    client.delete('http://my.test.com', headers=headers)

    make_request_mock.assert_called_once_with(
        'DELETE',
        'http://my.test.com',
        headers=headers
    )
