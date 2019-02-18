import json
import urllib.parse

import pytest
import responses

from slurmsdk.client import HTTPClient, merge_dict
from slurmsdk.exceptions import SDKException


def contain_headers(resp, headers):
    return resp.calls[0].request.headers.items() >= headers.items()


def has_queryparams(resp, params):
    query = urllib.parse.urlencode(params)
    return resp.calls[0].request.url.endswith('?' + query)


def has_body(resp, data):
    return json.loads(resp.calls[0].request.body) == data


@pytest.fixture
def mock_resp():
    with responses.RequestsMock() as resp:
        yield resp


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

    assert has_body(mock_resp, data)


def test_args_headers(mock_resp):
    url = 'https://fake.com'
    headers = {'header': 'value'}
    mock_resp.add('GET', url, content_type='application/json', json={})

    client = HTTPClient()
    client.make_request('GET', url, headers=headers)

    assert contain_headers(mock_resp, headers)


def test_args_params(mock_resp):
    url = 'https://fake.com'
    params = {'param': 'value'}
    mock_resp.add('GET', url, content_type='application/json', json={})

    client = HTTPClient()
    client.make_request('GET', url, params=params)

    assert has_queryparams(mock_resp, params)


def test_get(mock_resp):
    url = 'https://fake.com'
    headers = {'header': 'value'}
    params = {'param': 'value'}
    mock_resp.add('GET', url, content_type='application/json', json={})

    client = HTTPClient()
    result = client.get(url, headers=headers, params=params)

    assert contain_headers(mock_resp, headers)
    assert has_queryparams(mock_resp, params)
    assert result == {}


def test_post(mock_resp):
    url = 'https://fake.com'
    data = {'key': 'value'}
    headers = {'header': 'value'}
    mock_resp.add('POST', url, content_type='application/json', json={})

    client = HTTPClient()
    result = client.post(url, data=data, headers=headers)

    assert contain_headers(mock_resp, headers)
    assert has_body(mock_resp, data)
    assert result == {}


def test_put(mock_resp):
    url = 'https://fake.com'
    data = {'key': 'value'}
    headers = {'header': 'value'}
    mock_resp.add('PUT', url, content_type='application/json', json={})

    client = HTTPClient()
    result = client.put(url, data=data, headers=headers)

    assert contain_headers(mock_resp, headers)
    assert has_body(mock_resp, data)
    assert result == {}


def test_delete(mock_resp):
    url = 'https://fake.com'
    headers = {'header': 'value'}
    mock_resp.add('DELETE', url, content_type='application/json', json={})

    client = HTTPClient()
    result = client.delete(url, headers=headers)

    assert contain_headers(mock_resp, headers)
    assert result == {}
