"""Setup.py for the Label Studio Airflow provider package."""

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

"""Perform the package airflow-provider-label-studio setup."""
setup(
    name='airflow-provider-label-studio',
    version="0.0.1",
    description='Airflow package provider to perform action on Label Studio Platform.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        "apache_airflow_provider": [
            "provider_info=airflow.providers.label_studio.__init__:get_provider_info"
        ]
    },
    license='Apache License 2.0',
    packages=['airflow.providers.label_studio', 'airflow.providers.label_studio.hooks', 
    'airflow.providers.label_studio.operators',],
    install_requires=['apache-airflow>=2.0'],
    setup_requires=['setuptools', 'wheel'],
    author='Clement Parsy',
    author_email='cparsy@decideom.fr',
    url='',
    classifiers=[
        "Framework :: Apache Airflow",
        "Framework :: Apache Airflow :: Provider",
    ],
    python_requires='~=3.7',
)
