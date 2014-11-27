import os, sys

pwd = os.path.dirname(os.path.abspath(__file__))
print pwd

paths = os.path.dirname(__file__).split("/")

#this is for local deployment
#root_path = os.sep.join((os.environ['HOME'], 'local', 'pcapi'))
#this is for released ones
root_path = os.path.abspath(os.sep.join((pwd, '..', '..')))
print root_path

# append the root directory in your python system path
sys.path.append(os.path.join(root_path, 'pcapi'))

#print sys.path

## Change working directory so relative paths work
pwd = os.path.dirname(os.path.realpath(__file__))
os.chdir(pwd)

## Also add library to the python path
sys.path.append(os.path.join(root_path, 'lib'))
sys.path.append(pwd)

# activate the virtual environment
activate_this = os.path.join(root_path, "bin", "activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

# os.environ['ROOT_PATH'] = root_path

import bottle
import pcapi.routes
application = bottle.default_app()


if __name__ == "__main__":
    from pcapi.server import runserver
    runserver()

