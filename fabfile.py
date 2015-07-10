from contextlib import contextmanager
from fabric.api import env, hosts, cd, lcd, local, task, run, put, prefix, prompt, sudo
from fabric.contrib.project import rsync_project
import os, ConfigParser
import sys


"""
Two main uses:

1) Direct invocation
fab -H HOST -u USER --port PORT deploy

2) Using default values from configuration file under ./etc/fab.ini
fab server:cobweb deploy

"""

# GLOBALS
CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))
config=None

@contextmanager
def virtualenv(env):
    with prefix('source {0}/bin/activate'.format(env)):
        yield

@task
def server(serv):
    """Read default user,host,port values from ./etc/fab.ini"""
    env.hosts = [_config("hosts", serv),]
    env.user = _config("user", serv)
    env.port = _config("port", serv)
    if not ( env.port and env.user and env.hosts):
        print "Missing configuration values for " + `serv`
        sys.exit(1)

@task
def deploy(version='cobweb-dev'):
    """Rsync everything to server, pip installs as user and restarts apache"""

    REMOTE_PATH = os.path.join ( '~/dist/pcapi', version )

    local("""rsync -e"ssh -p%s" --exclude resources -C -av %s/ %s@%s:%s"""
    % (env.port, CURRENT_PATH, env.user, env.host, REMOTE_PATH ) )

    with cd(REMOTE_PATH):
        run("echo y | pip uninstall pcapi")
        run("pip install --user .")
        #sudo("/etc/init.d/httpd graceful")

@task
def deploy_with_venv(directory='dev'):
    """Install the current version to '~/dist/pcapi/releases/{directory}'"""

    local_path = './dist'
    remote_path = '~/dist/pcapi/releases'
    virtualenv_path = '{remote_path}/{directory}'.format(remote_path=remote_path, directory=directory)

    # Build the source distribution
    local('python setup.py sdist --formats=gztar')
    dist_name = local('python setup.py --fullname', capture=True)
    dist_file = '{dist_name}.tar.gz'.format(dist_name=dist_name)

    # Copy it to the server
    local('scp -P {port} {local_path}/{dist_file} {username}@{host}:/tmp'
        .format(local_path=local_path, dist_file=dist_file, username=env.user,
                host=env.host, port=env.port))

    # Initialize virtuelenv
    with cd(remote_path):
        run('virtualenv --no-site-packages {directory}'.format(remote_path, directory=directory))

    # Install the pcapi in the virtualenv
    with virtualenv(virtualenv_path):
        run('pip install /tmp/{dist_file}'.format(dist_file=dist_file))


def _config(var, section='install'):
    """ Read default values from fab.ini. Missing values are None """
    global config
    if config == None:
        config = ConfigParser.ConfigParser()
        conf_file = os.sep.join((CURRENT_PATH, 'etc', 'fab.ini'))
        config.read(conf_file)
    return config.get(section, var)
