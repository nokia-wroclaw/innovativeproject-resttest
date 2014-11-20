# coding=utf-8
from distutils.core import setup

setup(
    name='resttest',
    version='0.0.3',
    install_requires=[
        "requests",
    ],
    packages=['resttest'],
    url='https://github.com/nokia-wroclaw/innovativeproject-resttest',
    license='',
    author='Sławomir Domagała, Damian Mirecki, Tomasz Wlisłocki, Bartosz Zięba',
    author_email='',
    description='Tool for running rest-api tests written in plain language.'
)
