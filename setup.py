from setuptools import setup, find_packages


requires = [
    'requests>=2.21.0'
]


def get_version():
    with open('slurmsdk/version.py') as f:
        ns = {}
        exec(f.read(), ns)
        version = ns['__version__']
        return version


setup(
    name='SlurmSDK',
    version=get_version(),
    description='Slurm SDK for Python',
    license='MIT',
    python_requires='>=3.6',
    packages=find_packages(),
    install_requires=requires,
)
