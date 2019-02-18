import pytest

from slurmsdk.api import API, protected
from slurmsdk.exceptions import SDKException


def raise_auth_error(func, *args, **kwargs):
    with pytest.raises(SDKException) as exc:
        func(*args, **kwargs)

    return exc.value.message == 'Access token is required'


@pytest.fixture
def fake_get(monkeypatch):
    def func(self, url, headers=None, params=None):
        return {
            'url': url,
            'headers': headers,
            'params': params
        }

    monkeypatch.setattr('slurmsdk.client.HTTPClient.get', func)


@pytest.fixture
def fake_post(monkeypatch):
    def func(self, url, data=None, headers=None):
        return {
            'url': url,
            'data': data,
            'headers': headers
        }

    monkeypatch.setattr('slurmsdk.client.HTTPClient.post', func)


@pytest.fixture
def fake_delete(monkeypatch):
    def func(self, url, headers=None):
        return {
            'url': url,
            'headers': headers
        }

    monkeypatch.setattr('slurmsdk.client.HTTPClient.delete', func)


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
    assert raise_auth_error(instance.protected_method)


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


def test_authenticate(fake_post):
    username = 'user@test.com'
    password = 'pass'

    api = API('https://api.fake.com')
    result = api.authenticate(username, password)

    assert result['url'] == 'https://api.fake.com/auth/sign-in'
    assert result['data'] == {'username': username, 'password': password}


def test_create_user(fake_post):
    username = 'user@test.com'
    password = 'pass'

    api = API('https://api.fake.com', 'token')
    result = api.create_user(username, password)

    assert result['url'] == 'https://api.fake.com/users'
    assert result['data'] == {'username': username, 'password': password}
    assert result['headers'] == {'Authorization': 'Bearer token'}


def test_create_user_raises_access_token_required():
    api = API('https://api.fake.com')
    assert raise_auth_error(api.create_user, 'user@test.com', 'pass')


def test_list_users(fake_get):
    api = API('https://api.fake.com', 'token')
    result = api.list_users()

    assert result['url'] == 'https://api.fake.com/users'
    assert result['headers'] == {'Authorization': 'Bearer token'}
    assert result['params'] is None


def test_list_users_raises_access_token_required():
    api = API('https://api.fake.com')
    assert raise_auth_error(api.list_users)


def test_list_jobs(fake_get):
    api = API('https://api.fake.com', 'token')
    result = api.list_jobs()

    assert result['url'] == 'https://api.fake.com/jobs'
    assert result['headers'] == {'Authorization': 'Bearer token'}
    assert result['params'] == {'q': None, 'offset': None, 'limit': None}


def test_list_jobs_with_queryparams(fake_get):
    api = API('https://api.fake.com', 'token')
    result = api.list_jobs(q='query', offset=0, limit=1)

    assert result['url'] == 'https://api.fake.com/jobs'
    assert result['headers'] == {'Authorization': 'Bearer token'}
    assert result['params'] == {'q': 'query', 'offset': 0, 'limit': 1}


def test_list_jobs_raises_access_token_required():
    api = API('https://api.fake.com')
    assert raise_auth_error(api.list_jobs)


def test_pause_job(fake_post):
    api = API('https://api.fake.com', 'token')
    result = api.pause_job(1)

    assert result['url'] == 'https://api.fake.com/jobs/1/pause'
    assert result['data']is None
    assert result['headers'] == {'Authorization': 'Bearer token'}


def test_pause_job_raises_access_token_required():
    api = API('https://api.fake.com')
    assert raise_auth_error(api.pause_job, 1)


def test_resume_job(fake_post):
    api = API('https://api.fake.com', 'token')
    result = api.resume_job(1)

    assert result['url'] == 'https://api.fake.com/jobs/1/resume'
    assert result['data'] is None
    assert result['headers'] == {'Authorization': 'Bearer token'}


def test_resume_job_raises_access_token_required():
    api = API('https://api.fake.com')
    assert raise_auth_error(api.resume_job, 1)


def test_retry_job(fake_post):
    api = API('https://api.fake.com', 'token')
    result = api.retry_job(1)

    assert result['url'] == 'https://api.fake.com/jobs/1/retry'
    assert result['data'] is None
    assert result['headers'] == {'Authorization': 'Bearer token'}


def test_etry_job_raises_access_token_required():
    api = API('https://api.fake.com')
    assert raise_auth_error(api.retry_job, 1)


def test_delete_job(fake_delete):
    api = API('https://api.fake.com', 'token')
    result = api.delete_job(1)

    assert result['url'] == 'https://api.fake.com/jobs/1'
    assert result['headers'] == {'Authorization': 'Bearer token'}


def test_delete_job_raises_access_token_required():
    api = API('https://api.fake.com')
    assert raise_auth_error(api.delete_job, 1)
