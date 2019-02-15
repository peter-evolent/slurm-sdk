Slurm SDK
=========

This is the REST API client for Slurm. It requires Python 3.6 or higher.

## Quick Start

First, install the library:
```sh
pip install git+https://github.com/peter-evolent/slurm-sdk.git
```

Then, from a Python interpreter:

```python
    >>> import slurmsdk
    >>>
    >>> api = slurmsdk.API('https://slurm.evolenthealth.com')
    >>>
    >>> result = api.sign_in('user@evolenthealth.com', 'password')
    >>> api.access_token = result['access_token']
    >>>
    >>> for job in api.list_jobs(q='job_name'):
            print(job)
```

## Development

#### Gettinger Started

Assuming that you have Python and virtualenv installed, set up your environment and install the required dependencies:
```sh
$ git clone https://github.com/peter-evolent/slurm-sdk.git
$ cd slurm-sdk
$ virtualenv venv -p python3
...
$ source venv/bin/activate
$ make init
```

#### Running Tests

```sh
$ make test
```

#### Running Lint

```sh
$ make lint
```