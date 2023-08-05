from os import path
from setuptools import setup

THIS_DIR = path.dirname(__file__)
VERSION_FILE = path.join(THIS_DIR, '../VERSION')

version_file = open(VERSION_FILE)
version = version_file.read().strip()

setup(
    name='artfullylondon_ingestschema',

    version=version,
    python_requires='>=3.7',

    description='Domain schema for Artfully London ingest system',
    long_description='',

    author='Steve Johns',
    author_email='steve@stevejay.net',

    license='MIT License',

    packages=['artfullylondon.ingestschema'],
    zip_safe=False,

    package_data={
        'artfullylondon.ingestschema': ['*.json'],
    },
)
