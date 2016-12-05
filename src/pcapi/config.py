## This is a Singleton class to return values stored under resources/config.ini.
## Read that file for documentation of values.
## note to java coders: Singletons in python are just modules with plain functions.

"""
For an explanation of each config. item see comments in resource/config.ini
"""
from pcapi import api_version
from pkg_resources import resource_filename

import ConfigParser
import shutil
import os

config = ConfigParser.SafeConfigParser()

# set "home" variable for all configuration files
home = os.path.expanduser("~")
config.add_section('path')
config.set('path', 'home', home)


def get(section, key):
    return config.get(section, key)


def getboolean(section, key):
    return config.getboolean(section, key)
def has_option(section, option):
    return config.has_option(section, option)

def getCCMap():
    ccmap = {"Default": "",
             "Zero":"http://creativecommons.org/publicdomain/zero/1.0/",
             "CC-BY":"http://creativecommons.org/licenses/by/3.0",
             "CC-SA":"http://creativecommons.org/licenses/by-sa/3.0",
             "BY-NC-CA":"http://creativecommons.org/licenses/by-nc/3.0",
             "BY-NC-DC":"http://creativecommons.org/licenses/by-nc-nd/3.0"
             }
    return ccmap


# init config
# if a pcapi.ini file is found in more than one location
# the value from the latest added will be used


config_paths = []
conf_dir = os.path.join(home, '.pcapi')
config_paths.append(os.path.join(conf_dir, 'pcapi.ini'))
config_paths.append(os.path.join(conf_dir, api_version, 'pcapi.ini'))
config_paths.append(os.path.join('.', 'pcapi.ini'))
default_config_file = None

# combine the config files
found_paths = config.read(config_paths)

# fallback to bundled configuration file
if len(found_paths) == 0:
    print 'No config files found in the default locations tried:'
    for path in config_paths:
        print path
    print 'Creating default skeleton using default configuration'
    default_config_file = resource_filename(__name__, 'data/pcapi.ini')
    config.read(default_config_file)
else:
    print 'Loaded configuration from: ',
    for path in found_paths:
        print path

pcapi_path = config.get("path", "pcapi")
if not os.path.exists(pcapi_path):
    print 'Creating pcapi home directory: {0}'.format(pcapi_path)
    os.makedirs(pcapi_path)

# If still using default config file, copy it to pcapi_path
if default_config_file:
    shutil.copyfile(default_config_file, os.path.join(pcapi_path, 'pcapi.ini'))

log_path = config.get("path", "log_dir")
if not os.path.exists(log_path):
    print 'Creating logs directory: {0}'.format(log_path)
    os.makedirs(log_path)

data_path = config.get("path", "data_dir")
if not os.path.exists(data_path):
    print 'Creating data directory: {0}'.format(data_path)
    os.makedirs(data_path)

# Create OWS template file (normally under .pcapi/data/ows)
ows_tpl_path = config.get("path", "ows_template_dir")
if not os.path.exists(ows_tpl_path):
    print 'Creating data directory: {0}'.format(ows_tpl_path)
    os.makedirs(ows_tpl_path)
# copy ows templates from ~/.local/.../data/ to ~/.pcapi/...
ows_files = ['features.json', 'wfs_getcapabilities_response-1.0.0.tpl',
             'wfs_getcapabilities_response-1.1.0.tpl']
for f in ows_files:
    ows_file_path = os.path.join(ows_tpl_path,f)
    if not os.path.exists(ows_file_path):
        print 'Creating default %s' % ows_file_path
        default_features_file = resource_filename(__name__, 'data/{0}'.format(f))
        shutil.copyfile(default_features_file, ows_file_path)
