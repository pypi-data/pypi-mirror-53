"""Install jsonschema-typed."""

from setuptools import setup, find_packages
import os

dir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(dir, 'README.md')) as f:
    description = f.read()

setup(
    name='jsonschema-typed2',
    author='Connor Worley',
    author_email='connorbworley@gmail.com',
    url='https://github.com/connorworley/jsonschema-typed',
    python_requires='~=3.6',    # I think?
    license='MIT',
    version='0.3.1',
    packages=['jsonschema_typed'],
    zip_safe=False,
    install_requires=[
        'jsonschema==3.0.1',
        'mypy>=0.701'
    ],
    long_description=description,
    long_description_content_type='text/markdown'
)
