import os
import sys
import click
from github import Github

class GithubAPI(object):
    def __init__(self, org):
        self.api = Github(os.environ.get('GOM_GITHUB_TOKEN'))
        self.org = org

pass_github = click.make_pass_decorator(GithubAPI)

@click.group()
@click.option('--org', envvar='GOM_ORG', help='Changes the repository folder location.')
@click.version_option('0.1')
@click.pass_context
def cli(gom, org):
    """gom is a command line tool for interacting with your github
    organizations.
    """
    if os.environ.get('GOM_GITHUB_TOKEN') == None:
        sys.stderr.write("Error: missing required environment variable: GOM_GITHUB_TOKEN\n")
        exit(1)

    if org == None:
        sys.stderr.write("Error: either --org=<org> or GOM_ORG must be supplied\n")
        exit(1)

    # Create a Github object and remember it as as the context object. From
    # this point onwards other commands can refer to it by using the
    # @pass_github decorator.
    gom.obj = GithubAPI(org)

@cli.command()
@pass_github
def list_members(github):
    """Lists members of an organization.
    """
    for member in github.api.get_organization(github.org).get_members():
        print(member.login)

@cli.command()
@pass_github
def list_repos(github):
    """Lists repositories owned by an organization.
    """
    for repo in github.api.get_organization(github.org).get_repos():
        print(repo.name)

