from setuptools import setup

VERSION = '0.3.1.2'

setup(
    name='indor',
    version=VERSION,
    install_requires=[
        "requests",
        "pyparsing",
        'junit-xml',
        'termcolor',
        'beautifulsoup4'
    ],
    package_dir={'indor': 'src/indor'},
    packages=['indor'],
    package_data={'indor': ['logo.txt']},
    url='https://github.com/nokia-wroclaw/innovativeproject-resttest',
    license='',
    author='Sławomir Domagała, Damian Mirecki, Tomasz Wlisłocki, Bartosz Zięba',
    author_email='',
    description='Tool for running rest-api tests written in plain language.',
    entry_points={
        'console_scripts': [
            'indor = indor.main:main',
        ]
    }
)

