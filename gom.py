import os
import sys
import click
from github import Github

class GithubAPI(object):
    def __init__(self, org, dry_run):
        self.api = Github(os.environ.get('GOM_GITHUB_TOKEN'))
        self.dry_run = dry_run
        self.org = org
        self.member = []

    def require_org(self):
        if self.org == None:
            click.secho("Error: either --org=<org> or GOM_ORG must be supplied", fg='red')
            exit(1)

    def get_organization(self):
        self.require_org()
        return self.api.get_organization(self.org)

pass_github = click.make_pass_decorator(GithubAPI)

@click.group()
@click.option('--org',
        envvar='GOM_ORG',
        help='Organization name you are operating on.',
        required=False)
@click.option('--dry-run/--no-dry-run',
        help='Only print what would have been done.',
        required=False,
        default=False)
@click.option('--debug',
        help='Print debug messages to stdout.',
        required=False,
        is_flag=True)
@click.version_option('0.1')
@click.pass_context
def cli(gom, org, dry_run, debug):
    """gom is a command line tool for interacting with your github
    organizations.
    """
    if os.environ.get('GOM_GITHUB_TOKEN') == None:
        click.secho("Error: missing required environment variable: GOM_GITHUB_TOKEN", fg='red')
        exit(1)

    # Create a Github object and remember it as as the context object. From
    # this point onwards other commands can refer to it by using the
    # @pass_github decorator.
    gom.obj = GithubAPI(org, dry_run)
    if debug:
        from github import enable_console_debug_logging
        enable_console_debug_logging()

@cli.command()
@pass_github
def list_organizations(github):
    """Lists all the organizations you belong to.
    """
    for organization in github.api.get_user().get_orgs():
        print(organization.login)

@cli.command()
@pass_github
def list_members(github):
    """Lists members of an organization.
    """
    github.require_org
    for member in github.get_organization().get_members():
        print(member.login)

@cli.command()
@click.option('--role',
        type=click.Choice(['member', 'admin'],
        case_sensitive=False),
        default='member')
@click.argument('username')
@pass_github
def add_member(github, role, username):
    """Adds a member to the organization
    """
    _msg = 'Adding {} to organization {} in role {}'.format(username, github.org, role)
    if click.confirm('Add user {} to organization {} in role {}?'.format(
        username, github.org, role), default=False):
        if github.dry_run:
            click.secho('DRY RUN ' + _msg, fg='blue')
        else:
            click.secho(_msg, fg='green')
            github.get_organization().add_to_members(username, role)
    else:
        click.secho('Aborted! No changes made to organization.', fg='red')

@cli.command()
@pass_github
def list_repos(github):
    """Lists repositories owned by an organization.
    """
    github.require_org
    for repo in github.get_organization().get_repos():
        print(repo.name)

