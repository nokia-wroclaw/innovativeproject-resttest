# coding=utf-8
from distutils.core import setup

setup(
    name='indor',
    version='0.0.3.2',
    install_requires=[
        "requests",
        "pyparsing",
        'mock',
        'nose',
        'nose-cov'
    ],
    package_dir={'indor': 'indor/src'},
    packages=['indor'],
    package_data={'indor': ['logo.txt']},
    url='https://github.com/nokia-wroclaw/innovativeproject-resttest',
    license='',
    author='Sławomir Domagała, Damian Mirecki, Tomasz Wlisłocki, Bartosz Zięba',
    author_email='',
    description='Tool for running rest-api tests written in plain language.'
)
