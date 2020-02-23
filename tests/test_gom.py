import pytest
import re
import httpretty
from click.testing import CliRunner
from gom import cli

class JsonContent:
    """Serves up JSON content from files on disk."""
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return owner
        with open(f'tests/{self.name}.json') as file:
            setattr(instance, self.name, file.read())

        return getattr(instance, self.name)

class MockGithubResponse:
    organization = JsonContent('organization')
    organizations = JsonContent('organizations')
    members = JsonContent('members')

@pytest.fixture()
def httpmock():
    httpretty.enable()
    httpretty.reset()
    base_url = 'https://api.github.com'
    headers = {
            'content-type': 'application/json',
            'X-OAuth-Scopes': 'admin:org, admin:repo_hook, repo, user',
            'X-Accepted-OAuth-Scopes': 'repo'
            }
    fake = MockGithubResponse()
    response_mapping = {
            r'/user/orgs?': fake.organizations,
            r'/orgs/(\w+?)$': fake.organization,
            r'/orgs/(\w+?)/members$': fake.members,
            }
    for url, response in response_mapping.items():
        # Note: Here, I only bind `GET` methods, but you can bind any method you want
        httpretty.register_uri(
                httpretty.GET,
                re.compile(base_url + url),
                response,
                adding_headers=headers  # You need this!
                )
    yield "resource"
    httpretty.disable()

def test_cli_requires_an_org(monkeypatch, httpmock):
    """It errors if you don't provide --org"""
    monkeypatch.setenv('GOM_GITHUB_TOKEN', 'some-fake-token-123456')
    monkeypatch.delenv('GOM_ORG', raising=False)
    runner = CliRunner();
    result = runner.invoke(cli, ['list-members'])
    assert result.exit_code == 1
    assert 'Error: either --org=<org> or GOM_ORG must be supplied' in result.output

def test_cli_requires_a_token(monkeypatch, httpmock):
    """It errors if you don't provide a GOM_GITHUB_TOKEN env var"""
    monkeypatch.delenv('GOM_GITHUB_TOKEN', raising=False)
    monkeypatch.setenv('GOM_ORG', 'github')
    runner = CliRunner();
    result = runner.invoke(cli, ['list-members'])
    assert result.exit_code == 1
    assert 'Error: missing required environment variable: GOM_GITHUB_TOKEN' in result.output

def test_cli_reads_org_from_environment(monkeypatch, httpmock):
    """It can get the organization name from an env var"""
    monkeypatch.setenv('GOM_GITHUB_TOKEN', 'some-fake-token-123456')
    monkeypatch.setenv('GOM_ORG', 'github')
    runner = CliRunner();
    result = runner.invoke(cli, ['list-members'])
    assert result.exit_code == 0

def test_list_organizations(monkeypatch, httpmock):
    """It can retrieve all the organizations for a user"""
    monkeypatch.setenv('GOM_GITHUB_TOKEN', 'some-fake-token-123456')
    monkeypatch.setenv('GOM_ORG', 'github')
    runner = CliRunner();
    result = runner.invoke(cli, ['list-organizations'])
    assert result.exit_code == 0
    assert 'github' in result.output

def test_list_members(monkeypatch, httpmock):
    """It can retrieve all the members for an organizations"""
    monkeypatch.setenv('GOM_GITHUB_TOKEN', 'some-fake-token-123456')
    monkeypatch.setenv('GOM_ORG', 'github')
    runner = CliRunner();
    result = runner.invoke(cli, ['list-members'])
    assert result.exit_code == 0
    assert 'octocat' in result.output

def test_add_user_dry_run_works(monkeypatch):
    """It aborts when run with --dry-run option"""
    monkeypatch.setenv('GOM_GITHUB_TOKEN', 'some-fake-token-123456')
    monkeypatch.setenv('GOM_ORG', 'github')
    runner = CliRunner();
    result = runner.invoke(cli, ['--dry-run', 'add-member', 'octodog'], input='y\n')
    assert result.exit_code == 0
    assert 'DRY RUN' in result.output

def test_add_user_aborts_on_no(monkeypatch):
    """It aborts when run with --dry-run option"""
    monkeypatch.setenv('GOM_GITHUB_TOKEN', 'some-fake-token-123456')
    monkeypatch.setenv('GOM_ORG', 'github')
    runner = CliRunner();
    result = runner.invoke(cli, ['--dry-run', 'add-member', 'octodog'], input='n\n')
    assert result.exit_code == 0
    assert 'Aborted!' in result.output

