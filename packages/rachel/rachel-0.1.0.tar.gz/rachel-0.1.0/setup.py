import sys
from setuptools import setup, find_packages

setup(
    name='rachel',
    version='0.1.0',
    license='MIT',
    author='Ethan',
    author_email='ismewen@163.com',
    description="",
    packages=find_packages(),
    install_requires=[
        "Django==2.2.5",
        "djangorestframework==3.10.3",
        "Werkzeug==0.16.0"
    ]
)