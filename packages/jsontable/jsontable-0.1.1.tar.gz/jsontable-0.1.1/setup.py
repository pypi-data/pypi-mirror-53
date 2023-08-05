from setuptools import setup, find_packages, Extension
from os import path

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='jsontable',
    version='0.1.1',
    description='Convert a JSON to a table',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/ernestomonroy/jsontable',
    author='Ernesto Monroy',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    keywords='json mining etl extract transform etltools data parsing parse mapper relational table',
    packages=find_packages(include=['jsontable']),
    python_requires='>=3.5',
    project_urls={
        'Bug Reports': 'https://github.com/ernestomonroy/jsontable/issues',
        'Source': 'https://github.com/ernestomonroy/jsontable',
    },
)