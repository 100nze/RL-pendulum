from setuptools import setup, find_packages

setup(
    name = 'pendulumrl',
    version = '0.1.0',
    description = 'A reinforcement learning library for pendulum control',
    package_dir={'': 'files'},  
    packages=find_packages(where='files'),
)

