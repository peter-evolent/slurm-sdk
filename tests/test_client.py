import json
from unittest.mock import Mock

import pytest
import responses

from slurmsdk.client import HTTPClient, merge_dict
from slurmsdk.exceptions import SDKException


@pytest.fixture
def mock_resp():
    with responses.RequestsMock() as resp:
        yield resp


@pytest.fixture
def mock_make_request(monkeypatch):
    mock = Mock()
    monkeypatch.setattr(HTTPClient, 'make_request', mock)
    return mock


def test_merge_dict():
    assert merge_dict({'a': 1}, {'b': 1}) == {'a': 1, 'b': 1}


def test_merge_dict_update():
    assert merge_dict({'a': 1}, {'a': 2}) == {'a': 2}


def test_request_content_type_header(mock_resp):
    url = 'https://fake.com'
    mock_resp.add('GET', url, content_type='application/json', json={})

    client = HTTPClient()
    client.make_request('GET', url)

    assert mock_resp.calls[0].request.headers['content-type'] == 'application/json'


def test_valid_json_response(mock_resp):
    url = 'https://fake.com'
    resp_data = {'key': 'value'}
    mock_resp.add('GET', url, status=200,
                  content_type='application/json', json=resp_data)

    client = HTTPClient()
    resp = client.make_request('GET', url)

    assert resp == resp_data


def test_valid_json_error_response(mock_resp):
    url = 'https://fake.com'
    resp_data = {'key': 'value'}
    mock_resp.add('GET', url, status=400,
                  content_type='application/json', json=resp_data)

    client = HTTPClient()
    with pytest.raises(SDKException) as exc:
        client.make_request('GET', url)

    assert exc.value.message == 400
    assert exc.value.data == resp_data


def test_connection_error(mock_resp):
    url = 'https://fake.com'

    client = HTTPClient()
    with pytest.raises(SDKException) as exc:
        client.make_request('GET', url)

    assert url in exc.value.message


def test_invalid_response_content_type(mock_resp):
    url = 'https://fake.com'
    mock_resp.add('GET', url, status=200, content_type='plain/text')

    client = HTTPClient()
    with pytest.raises(SDKException) as exc:
        client.make_request('GET', url)

    assert exc.value.message == 'Invalid Content-Type: plain/text'


def test_non_json_response(mock_resp):
    url = 'https://fake.com'
    text = 'response body'
    mock_resp.add('GET', url, status=200, content_type='application/json', body=text)

    client = HTTPClient()
    with pytest.raises(SDKException) as exc:
        client.make_request('GET', url)

    assert 'Invalid JSON response' in exc.value.message


def test_args_data(mock_resp):
    url = 'https://fake.com'
    data = {'header': 'value'}
    mock_resp.add('GET', url, content_type='application/json', json={})

    client = HTTPClient()
    client.make_request('GET', url, data=data)

    assert json.loads(mock_resp.calls[0].request.body) == data


def test_args_headers(mock_resp):
    url = 'https://fake.com'
    headers = {'header': 'value'}
    mock_resp.add('GET', url, content_type='application/json', json={})

    client = HTTPClient()
    client.make_request('GET', url, headers=headers)

    assert mock_resp.calls[0].request.headers.items() >= headers.items()


def test_args_params(mock_resp):
    url = 'https://fake.com'
    params = {'param': 'value'}
    mock_resp.add('GET', url, content_type='application/json', json={})

    client = HTTPClient()
    client.make_request('GET', url, params=params)

    assert mock_resp.calls[0].request.url.endswith('?param=value')


def test_get(mock_make_request):
    headers = {'header': 'value'}
    params = {'param': 'value'}

    client = HTTPClient()
    client.get('https://fake.com', headers=headers, params=params)

    mock_make_request.assert_called_once_with(
        'GET',
        'https://fake.com',
        headers=headers,
        params=params
    )


def test_post(mock_make_request):
    data = {'key': 'value'}
    headers = {'header': 'value'}

    client = HTTPClient()
    client.post('https://fake.com', data=data, headers=headers)

    mock_make_request.assert_called_once_with(
        'POST',
        'https://fake.com',
        data=data,
        headers=headers
    )


def test_put(mock_make_request):
    data = {'key': 'value'}
    headers = {'header': 'value'}

    client = HTTPClient()
    client.put('https://fake.com', data=data, headers=headers)

    mock_make_request.assert_called_once_with(
        'PUT',
        'https://fake.com',
        data=data,
        headers=headers
    )


def test_delete(mock_make_request):
    headers = {'header': 'value'}

    client = HTTPClient()
    client.delete('https://fake.com', headers=headers)

    mock_make_request.assert_called_once_with(
        'DELETE',
        'https://fake.com',
        headers=headers
    )
