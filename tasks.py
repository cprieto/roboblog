import os, sys
import coloredlogs, logging
import pelicanconf
import publishconf

from invoke import task
from git import Repo

join = os.path.join
normpath = os.path.normpath


def full_path(x): return join(os.path.dirname(os.path.realpath(__file__)), x)


output_path = full_path(pelicanconf.OUTPUT_PATH)
blog_path = os.path.dirname(os.path.realpath(__file__))

coloredlogs.install()


@task
def clean(ctx):
    repo = Repo(blog_path)

    if any(normpath(x.abspath) == normpath(output_path) for x in repo.submodules):
        logging.warn("Output directory is a git submodule, resetting it.")
        output = Repo(output_path)
        output.head.reset(working_tree=True, hard=True)
        output.git.clean("-f")
    else:
        logging.warn("Output path is not a git submodule, deleting it.")
        ctx.run("rm -rf {0}", pelicanconf.OUTPUT_PATH)


@task
def build(ctx):
    logging.info("Generating blog at {0}".format(pelicanconf.OUTPUT_PATH))
    ctx.run("pelican -s pelicanconf.py")


@task
def rebuild(ctx):
    clean(ctx)
    build(ctx)


@task
def regenerate(ctx):
    ctx.run("pelican -s -r pelicanconf.py")


@task
def preview(ctx):
    logging.info("Generating publish version at {0}.".format(publishconf.OUTPUT_PATH))
    ctx.run("pelican -s publishconf.py")


@task
def publish(ctx):
    clean(ctx)
    create_submodule(ctx)
    update_submodule(ctx)
    fetch_submodule(ctx)

    #preview(ctx)

    #output = Repo(full_path(publishconf.OUTPUT_PATH))

    # if output.is_dirty():
    #     # Adding untracked files
    #     output.index.add(x for x in output.untracked_files)
    #
    #     # Adding modified files
    #     output.index.add(x.a_path for x in output.index.diff(None) if x.change_type == 'M')
    #
    #     ctx.run("git --git-dir={0}/.git commit".format(output.working_tree_dir), pty=True)
    #
    # else:
    #     logging.info("No changes made to the blog!")


@task
def create_submodule(ctx):
    repo = Repo(blog_path)
    if not (repo.submodule(publishconf.SUBMODULE_NAME).module_exists()):
        logging.warn("Output submodule {0} doesn't exists, creating it at {1}.".format(
            publishconf.SUBMODULE_NAME, publishconf.OUTPUT_PATH))

        repo.create_submodule(url=publishconf.GITHUB_REPO, name=publishconf.SUBMODULE_NAME,
                              path=publishconf.OUTPUT_PATH, branch="master")


@task
def update_submodule(ctx):
    repo = Repo(blog_path)
    repo.submodule_update(init=True)

@task
def fetch_submodule(ctx):
    output = Repo(full_path(publishconf.OUTPUT_PATH))
    output.remote("origin").pull("master")

    repo = Repo(blog_path)
    if any(x for x in repo.index.diff(None) if normpath(x.a_path) == normpath(publishconf.OUTPUT_PATH)):
        logging.warn("Updating submodule to latest version")
        repo.git.add(publishconf.OUTPUT_PATH)
        repo.index.commit(message="Updated output to latest version in remote")