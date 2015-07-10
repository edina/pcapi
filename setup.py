from pcapi import version
from setuptools import setup, find_packages

setup(
    name="pcapi",
    version='{0}.0'.format(version),
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,

    package_data={
        'pcapi': ['data/*',],
    },

    install_requires=['Wand==0.3.8',
                      'beautifulsoup4==4.1.3',
                      'bottle==0.11.4',
                      'dropbox==1.5.1',
                      'html5lib==0.999',
                      'lxml==3.1.2',
                      'simplekml==1.2.1',
                      'threadpool==1.2.7',
                      'WebTest==2.0.4',
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
