from setuptools import setup, find_packages

setup(
    name="pcapi",
    version="0.4",
    packages=find_packages('src'),
    package_dir={'': 'src'},

    data_files=[('resources', ['src/resources/pcapi.ini.example'])],

    install_requires=['Wand==0.3.8',
                      'beautifulsoup4==4.1.3',
                      'bottle==0.11.4',
                      'dropbox==1.5.1',
                      'html5lib==0.95',
                      'lxml==3.1.2',
                      'simplekml==1.2.1',
                      'threadpool==1.2.7',
                      'WebTest==2.0.4',
                      'Jinja2==2.7.2',
                      'pysqlite==2.6.3',
                      'argparse==1.2.1'],
    dependency_links=[
        # Use custom pysqlite with the LOAD_EXTENSION enabled
        'https://github.com/edina/pysqlite/archive/2.6.3.tar.gz#egg=pysqlite-2.6.3'
    ],

    entry_points={
        'console_scripts': [
            'pcapi-admin = pcapi.utils.admin:parse_commandline'
        ]
    }
)
