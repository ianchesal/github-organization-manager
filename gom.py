import os
import sys
import click
from github import Github, NamedUser

class GOM(object):
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

pass_gom = click.make_pass_decorator(GOM)

def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()

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

    # Create a GOM object and remember it as as the context object. From
    # this point onwards other commands can refer to it by using the
    # @pass_gom decorator.
    gom.obj = GOM(org, dry_run)
    if debug:
        from github import enable_console_debug_logging
        enable_console_debug_logging()

@cli.command()
@pass_gom
def list_organizations(gom):
    """Lists all the organizations you belong to.
    """
    for organization in gom.api.get_user().get_orgs():
        print(organization.login)

@cli.command()
@pass_gom
def list_members(gom):
    """Lists members of an organization.
    """
    gom.require_org
    for member in gom.get_organization().get_members():
        print(member.login)

@cli.command()
@click.argument('username')
@pass_gom
def check_member(gom, username):
    """Check if a user is a member of an organization.
    """
    gom.require_org
    user = gom.api.get_user(username)
    if gom.get_organization().has_in_members(user):
        print('User {} is in organization {}'.format(
            username, gom.org))
        exit(0)
    print('User {} is NOT in organization {}'.format(
        username, gom.org))
    exit(1)

@cli.command()
@click.option('--role',
        type=click.Choice(['member', 'admin'],
        case_sensitive=False),
        default='member',
        help='The role to use for the users')
@click.option('--yes',
        is_flag=True,
        callback=abort_if_false,
        expose_value=False,
        prompt='Are you sure you want to add members to the organization?',
        help='Execute command without asking for confirmation')
@click.argument('usernames', nargs=-1)
@pass_gom
def add_members(gom, role, usernames):
    """Adds members to the organization
    """
    for username in usernames:
        _msg = 'Added {} to organization {} in role {}'.format(username, gom.org, role)
        if gom.dry_run:
            click.secho('DRY RUN ' + _msg, fg='blue')
        else:
            gom.get_organization().add_to_members(username, role)
            click.secho(_msg, fg='green')

@cli.command()
@click.option('--yes',
        is_flag=True,
        callback=abort_if_false,
        expose_value=False,
        prompt='Are you sure you want to remove members from the organization?',
        help='Execute command without asking for confirmation')
@click.argument('usernames', nargs=-1)
@pass_gom
def remove_members(gom, usernames):
    """Removes members from the organization
    """
    for username in usernames:
        _msg = 'Removed {} from organization {}'.format(username, gom.org)
        user = gom.api.get_user(username)
        if not gom.get_organization().has_in_members(user):
            click.secho('Error: User {} is not in organization {}'.format(
                username, gom.org))
            exit(1)
        if gom.dry_run:
            click.secho('DRY RUN ' + _msg, fg='blue')
        else:
            click.secho(_msg, fg='green')
            gom.get_organization().remove_from_members(user)

@cli.command()
@pass_gom
def list_repos(gom):
    """Lists repositories owned by an organization.
    """
    gom.require_org
    for repo in gom.get_organization().get_repos():
        print(repo.name)

