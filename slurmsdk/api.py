"""Slurm REST API Client"""
from functools import wraps
from typing import List

from slurmsdk.client import HTTPClient
from slurmsdk.exceptions import SDKException


def protected(f):
    """Protects method using

    Raises:
        SDKException: if access_token is not set
    """
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        if self.access_token is None:
            raise SDKException('Access token is required')
        return f(self, *args, **kwargs)
    return wrapper


class API:
    """Slurm REST API"""
    def __init__(self, base_url: str, access_token: str = None):
        self.base_url = base_url.rstrip('/')
        self.access_token = access_token
        self.client = HTTPClient()

    @property
    def auth_header(self) -> dict:
        """Returns Auhtorization header"""
        return {'Authorization': f'Bearer {self.access_token}'}

    def authenticate(self, username: str, password: str) -> dict:
        """Authenticates with usercreds"""
        endpoint = f'{self.base_url}/auth/sign-in'
        payload = {'username': username, 'password': password}
        return self.client.post(endpoint, data=payload)

    @protected
    def create_user(self, username: str, password: str) -> dict:
        """Creates a user"""
        endpoint = f'{self.base_url}/users'
        payload = {'username': username, 'password': password}
        return self.client.post(endpoint, data=payload, headers=self.auth_header)

    @protected
    def list_users(self) -> List[dict]:
        """Returns a list of users"""
        endpoint = f'{self.base_url}/users'
        return self.client.get(endpoint, headers=self.auth_header)

    @protected
    def list_jobs(self, q: str = None, offset: int = None, limit: int = None) -> List[dict]:
        """Returns a list of jobs

        Args:
            q: search query
            offset: offset of the first row
            limit: limit the number of rows returned
        """
        endpoint = f'{self.base_url}/jobs'
        params = {'q': q, 'offset': offset, 'limit': limit}
        return self.client.get(endpoint, headers=self.auth_header, params=params)

    @protected
    def pause_job(self, job_id: int) -> dict:
        """Pauses a job"""
        endpoint = f'{self.base_url}/jobs/{job_id}/pause'
        return self.client.post(endpoint, headers=self.auth_header)

    @protected
    def resume_job(self, job_id: int) -> dict:
        """Resumes a job"""
        endpoint = f'{self.base_url}/jobs/{job_id}/resume'
        return self.client.post(endpoint, headers=self.auth_header)

    @protected
    def retry_job(self, job_id: int) -> dict:
        """Re-runs a job"""
        endpoint = f'{self.base_url}/jobs/{job_id}/retry'
        return self.client.post(endpoint, headers=self.auth_header)

    @protected
    def delete_job(self, job_id: int) -> dict:
        """Deletes a job"""
        endpoint = f'{self.base_url}/jobs/{job_id}'
        return self.client.delete(endpoint, headers=self.auth_header)
