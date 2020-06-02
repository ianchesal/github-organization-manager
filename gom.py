import os
import click
import logging
from rich.logging import RichHandler
from github import Github


class GOM(object):
    def __init__(self, dry_run):
        self.org = os.environ.get('GOM_ORG')
        self.base_url = 'https://api.github.com'
        if os.environ.get('GOM_BASE_URL'):
            self.base_url = os.environ.get('GOM_BASE_URL')
        self.api = Github(base_url=self.base_url, login_or_token=os.environ.get('GOM_GITHUB_TOKEN'))
        self.dry_run = dry_run
        self.member = []

    def get_organization(self):
        return self.api.get_organization(self.org)


pass_gom = click.make_pass_decorator(GOM)


def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()


@click.group()
@click.option(
    '--dry-run/--no-dry-run',
    help='Only print what would have been done.',
    required=False,
    default=False)
@click.option(
    '--debug',
    help='Print debug messages to stdout.',
    required=False,
    is_flag=True)
@click.version_option('0.1')
@click.pass_context
def cli(gom, dry_run, debug):
    """gom is a command line tool for interacting with your github
    organizations.
    """
    if debug:
        logging.basicConfig(level=logging.DEBUG, format="%(message)s", datefmt="[%X] ", handlers=[RichHandler()])
        # Uncomment this if you want to see the raw requests and responses by the PyGithub API
        # Warning: it produces a TON of debug output
        # from github import enable_console_debug_logging
        # enable_console_debug_logging()
    else:
        logging.basicConfig(level=logging.INFO, format="%(message)s", datefmt="[%X] ", handlers=[RichHandler()])
    if os.environ.get('GOM_GITHUB_TOKEN') is None:
        click.secho("Error: missing required environment variable: GOM_GITHUB_TOKEN", fg='red')
        exit(1)

    # Create a GOM object and remember it as as the context object. From
    # this point onwards other commands can refer to it by using the
    # @pass_gom decorator.
    gom.obj = GOM(dry_run)


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
    print('Memeber ID, Name, Email, Role, Updated At, Suspended At')
    for member in gom.get_organization().get_members():
        membership = member.get_organization_membership(gom.org)
        print(f'{member.login}, {member.name}, {member.email}, {membership.role}, {member.updated_at}, {member.suspended_at}')


@cli.command()
@click.argument('username')
@pass_gom
def check_member(gom, username):
    """Check if a user is a member of an organization.
    """
    user = gom.api.get_user(username)
    if gom.get_organization().has_in_members(user):
        print('User {} is in organization {}'.format(
            username, gom.org))
        exit(0)
    print('User {} is NOT in organization {}'.format(
        username, gom.org))
    exit(1)


@cli.command()
@click.option(
    '--role',
    type=click.Choice(
        ['member', 'admin'],
        case_sensitive=False),
    default='member',
    help='The role to use for the users')
@click.option(
    '--yes',
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
            user = gom.api.get_user(username)
            gom.get_organization().add_to_members(user, role)
            click.secho(_msg, fg='green')


@cli.command()
@click.option(
    '--yes',
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
@click.option(
    '--repo-type',
    type=click.Choice(
        ['all', 'public', 'private', 'forks', 'sources', 'member'],
        case_sensitive=True),
    default='all',
    help='List only a specific type of repository owned by the organization')
@pass_gom
def list_repos(gom, repo_type):
    """Lists repositories owned by an organization.
    """
    for repo in gom.get_organization().get_repos(type=repo_type):
        print(repo.name)
