from setuptools import setup, find_packages

VERSION = '0.4.dev1'

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
    packages=find_packages('./src'),
    include_package_data=True,
    package_data={'indor': ['logo.txt']},
    package_dir={'': './src'},
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

