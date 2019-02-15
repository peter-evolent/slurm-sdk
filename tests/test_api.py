from unittest.mock import Mock

import pytest

from slurmsdk.api import API, protected
from slurmsdk.exceptions import SDKException


def assert_protected(func, *args, **kwargs):
    with pytest.raises(SDKException) as exc:
        func(*args, **kwargs)

    assert exc.value.message == 'Access token is required'


@pytest.fixture
def mock_get(monkeypatch):
    mock = Mock()
    monkeypatch.setattr('slurmsdk.client.HTTPClient.get', mock)
    return mock


@pytest.fixture
def mock_post(monkeypatch):
    mock = Mock()
    monkeypatch.setattr('slurmsdk.client.HTTPClient.post', mock)
    return mock


@pytest.fixture
def mock_delete(monkeypatch):
    mock = Mock()
    monkeypatch.setattr('slurmsdk.client.HTTPClient.delete', mock)
    return mock


def test_protected():
    class A:
        def __init__(self):
            self.access_token = 'not none'

        @protected
        def protected_method(self):
            pass

    instance = A()
    instance.protected_method()


def test_protected_without_access_token():
    class A:
        def __init__(self):
            self.access_token = None

        @protected
        def protected_method(self):
            pass

    instance = A()
    assert_protected(instance.protected_method)


def test_sanitize_base_url():
    api = API('https://api.fake.com/')
    assert api.base_url == 'https://api.fake.com'


def test_access_token():
    api = API('https://api.fake.com', access_token='token')
    assert api.access_token == 'token'


def test_update_access_token():
    api = API('https://api.fake.com', access_token='token')
    api.access_token = 'new token'
    assert api.auth_header == {'Authorization': 'Bearer new token'}


def test_authenticate(mock_post):
    username = 'user@test.com'
    password = 'pass'

    api = API('https://api.fake.com')
    result = api.authenticate(username, password)

    mock_post.assert_called_once_with(
        'https://api.fake.com/auth/sign-in',
        data={'username': username, 'password': password},
    )
    result == mock_post


def test_create_user(mock_post):
    username = 'user@test.com'
    password = 'pass'

    api = API('https://api.fake.com', 'token')
    result = api.create_user(username, password)

    mock_post.assert_called_once_with(
        'https://api.fake.com/users',
        data={'username': username, 'password': password},
        headers={'Authorization': 'Bearer token'}
    )
    result == mock_post


def test_create_user_raises_access_token_required():
    api = API('https://api.fake.com')
    assert_protected(api.create_user, 'user@test.com', 'pass')


def test_list_users(mock_get):
    api = API('https://api.fake.com', 'token')
    result = api.list_users()

    mock_get.assert_called_once_with(
        'https://api.fake.com/users',
        headers={'Authorization': 'Bearer token'}
    )
    result == mock_get


def test_list_users_raises_access_token_required():
    api = API('https://api.fake.com')
    assert_protected(api.list_users)


def test_list_jobs(mock_get):
    api = API('https://api.fake.com', 'token')
    result = api.list_jobs()

    mock_get.assert_called_once_with(
        'https://api.fake.com/jobs',
        headers={'Authorization': 'Bearer token'},
        params={'q': None, 'offset': None, 'limit': None}
    )
    result == mock_get


def test_list_jobs_with_queryparams(mock_get):
    api = API('https://api.fake.com', 'token')
    result = api.list_jobs(q='query', offset=0, limit=1)

    mock_get.assert_called_once_with(
        'https://api.fake.com/jobs',
        headers={'Authorization': 'Bearer token'},
        params={'q': 'query', 'offset': 0, 'limit': 1}
    )
    result == mock_get


def test_list_jobs_raises_access_token_required():
    api = API('https://api.fake.com')
    assert_protected(api.list_jobs)


def test_pause_job(mock_post):
    api = API('https://api.fake.com', 'token')
    result = api.pause_job(1)

    mock_post.assert_called_once_with(
        'https://api.fake.com/jobs/1/pause',
        headers={'Authorization': 'Bearer token'}
    )
    result == mock_post


def test_pause_job_raises_access_token_required():
    api = API('https://api.fake.com')
    assert_protected(api.pause_job, 1)


def test_resume_job(mock_post):
    api = API('https://api.fake.com', 'token')
    result = api.resume_job(1)

    mock_post.assert_called_once_with(
        'https://api.fake.com/jobs/1/resume',
        headers={'Authorization': 'Bearer token'}
    )
    result == mock_post


def test_resume_job_raises_access_token_required():
    api = API('https://api.fake.com')
    assert_protected(api.resume_job, 1)


def test_retry_job(mock_post):
    api = API('https://api.fake.com', 'token')
    result = api.retry_job(1)

    mock_post.assert_called_once_with(
        'https://api.fake.com/jobs/1/retry',
        headers={'Authorization': 'Bearer token'}
    )
    result == mock_post


def test_etry_job_raises_access_token_required():
    api = API('https://api.fake.com')
    assert_protected(api.retry_job, 1)


def test_delete_job(mock_delete):
    api = API('https://api.fake.com', 'token')
    result = api.delete_job(1)

    mock_delete.assert_called_once_with(
        'https://api.fake.com/jobs/1',
        headers={'Authorization': 'Bearer token'}
    )
    result == mock_post


def test_delete_job_raises_access_token_required():
    api = API('https://api.fake.com')
    assert_protected(api.delete_job, 1)
