"""Setup tools configuration file"""
from setuptools import setup, find_packages

setup(
    name="pcapi",
    version="1.4",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,

    package_data={
        'pcapi': ['data/*',],
    },

    install_requires=['bottle==0.11.4',
                      'WebTest==2.0.20',
                      'psycopg2==2.5.3',
                      'pysqlite==2.6.3',
                      'ppygis==0.2'],

    zip_safe=True,
    entry_points={
        'console_scripts': [
            'pcapi = pcapi.server:runserver',
            'pcapi_upgrade = pcapi.utils.pcapi_upgrade:upgrade_all_data'
        ]
    }
)
