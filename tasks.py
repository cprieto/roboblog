import os
import shutil
import sys
import datetime

from invoke import task
from invoke.util import cd
from pelican.server import ComplexHTTPRequestHandler, RootedHTTPServer
from pelican.settings import DEFAULT_CONFIG, get_settings_from_file

CONFIG = {
    # Local path configuration (can be absolute or relative to tasks.py)
    'deploy_path': 'output',
    # Github Pages configuration
    'github_pages_branch': 'gh-pages',
    'commit_message': "'Publish site on {}'".format(datetime.date.today().isoformat()),
    # Port for `serve`
    'port': 8000,
    # Remote github page site
    'github_pages_repo': 'git@github.com:cprieto/cprieto.github.io.git',
    # Remote github page branch
    'github_pages_remote_branch': 'master',

    'site_domain': 'cprieto.com'
}

SETTINGS = {}
SETTINGS.update(DEFAULT_CONFIG)
LOCAL_SETTINGS = get_settings_from_file('pelicanconf.py')
SETTINGS.update(LOCAL_SETTINGS)

@task
def clean(c):
    """Remove generated files"""
    if os.path.isdir(CONFIG['deploy_path']):
        shutil.rmtree(CONFIG['deploy_path'])
        os.makedirs(CONFIG['deploy_path'])

@task
def build(c):
    """Build local version of site"""
    c.run('pelican -s pelicanconf.py')

@task
def rebuild(c):
    """`build` with the delete switch"""
    c.run('pelican -d -s pelicanconf.py')

@task
def regenerate(c):
    """Automatically regenerate site upon file modification"""
    c.run('pelican -r -s pelicanconf.py')

@task
def serve(c):
    """Serve site at http://localhost:8000/"""

    class AddressReuseTCPServer(RootedHTTPServer):
        allow_reuse_address = True

    server = AddressReuseTCPServer(
        CONFIG['deploy_path'],
        ('', CONFIG['port']),
        ComplexHTTPRequestHandler)

    sys.stderr.write('Serving on port {port} ...\n'.format(**CONFIG))
    server.serve_forever()

@task
def preview(c):
    """Build production version of site"""
    c.run('pelican -s publishconf.py')


@task
def publish(c):
    """Publish to production via rsync"""
    c.run('pelican -s publishconf.py')
    c.run(
        'rsync --delete --exclude ".DS_Store" -pthrvz -c '
        '{} {production}:{dest_path}'.format(
            CONFIG['deploy_path'].rstrip('/') + '/',
            **CONFIG))

@task
def gh_pages(c):
    """Publish to GitHub Pages"""
    preview(c)
    print('Running ghp-import')
    c.run('ghp-import {deploy_path} -b {github_pages_branch} -c {site_domain}'.format(**CONFIG))
    print('Pushing to GH')
    c.run('git push -f {github_pages_repo} {github_pages_branch}:{github_pages_remote_branch}'.format(**CONFIG))

@task
def livereload(c):
    """Automatically reload browser tab upon file modification."""
    from livereload import Server
    build(c)
    server = Server()
    deploy_path = CONFIG['deploy_path']
    content_path = SETTINGS['PATH']
    content_file_extensions = ['.md', '.rst']
    for file_extension in content_file_extensions:
        content_blob = '{0}/**/*{1}'.format(content_path, file_extension)
        server.watch(content_blob, lambda: build(c))
    server.serve(root=deploy_path)
