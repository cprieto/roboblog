from fabric.api import *
import fabric.contrib.project as project
import os
import shutil
import sys
import SocketServer

from pelican.server import ComplexHTTPRequestHandler

# Local path configuration (can be absolute or relative to fabfile)
env.deploy_path = 'output'
DEPLOY_PATH = env.deploy_path


# Port for `serve`
PORT = 8000

def clean():
    """Remove generated files"""
    if os.path.isdir(DEPLOY_PATH):
        shutil.rmtree(DEPLOY_PATH)
        os.makedirs(DEPLOY_PATH)

def build():
    """Build local version of site"""
    local('pelican -s pelicanconf.py')

def rebuild():
    """`clean` then `build`"""
    clean()
    build()

def regenerate():
    """Automatically regenerate site upon file modification"""
    local('pelican -r -s pelicanconf.py')

def serve():
    """Serve site at http://localhost:8000/"""
    os.chdir(env.deploy_path)

    class AddressReuseTCPServer(SocketServer.TCPServer):
        allow_reuse_address = True

    server = AddressReuseTCPServer(('', PORT), ComplexHTTPRequestHandler)

    sys.stderr.write('Serving on port {0} ...\n'.format(PORT))
    server.serve_forever()

def reserve():
    """`build`, then `serve`"""
    build()
    serve()

def preview():
    """Build production version of site"""
    local('pelican -s publishconf.py')

def publish():
    """Publish to production to github pages"""
    current_dir = os.path.abspath(os.path.dirname(__file__))
    sys.path.append('.')
    from publishconf import OUTPUT_PATH,GITHUB_REPO
    if os.path.isdir(OUTPUT_PATH) and os.path.exists(OUTPUT_PATH):
        print 'Removing output directory...'
        shutil.rmtree(OUTPUT_PATH)
    os.mkdir(OUTPUT_PATH)
    os.chdir(OUTPUT_PATH)
    local('git clone ' + GITHUB_REPO + ' .')
    os.chdir(current_dir)
    local('pelican -s publishconf.py')
    os.chdir(OUTPUT_PATH)
    local('git add .')
    local('git commit')

