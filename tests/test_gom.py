import pytest
from click.testing import CliRunner
from gom import cli


def test_cli_requires_an_org(monkeypatch):
    """It errors if you don't provide --org"""
    monkeypatch.delenv('GOM_ORG', raising=False)
    runner = CliRunner();
    result = runner.invoke(cli, ['list-members'])
    assert result.exit_code == 1
    assert 'Error: either --org=<org> or GOM_ORG must be supplied' in result.output


def test_cli_requires_a_token(monkeypatch):
    """It errors if you don't provide a GOM_GITHUB_TOKEN env var"""
    monkeypatch.delenv('GOM_GITHUB_TOKEN', raising=False)
    runner = CliRunner();
    result = runner.invoke(cli, ['list-members'])
    assert result.exit_code == 1
    assert 'Error: missing required environment variable: GOM_GITHUB_TOKEN' in result.output


@pytest.mark.vcr()
def test_cli_reads_org_from_environment(monkeypatch):
    """It can get the organization name from an env var"""
    runner = CliRunner();
    result = runner.invoke(cli, ['list-members'])
    assert result.exit_code == 0


@pytest.mark.vcr()
def test_list_organizations(monkeypatch):
    """It can retrieve all the organizations for a user"""
    runner = CliRunner();
    result = runner.invoke(cli, ['list-organizations'])
    assert result.exit_code == 0
    assert 'tinwhiskersband' in result.output


@pytest.mark.vcr()
def test_list_members(monkeypatch):
    """It can retrieve all the members for an organizations"""
    runner = CliRunner();
    result = runner.invoke(cli, ['list-members'])
    assert result.exit_code == 0
    assert 'ianchesal' in result.output


def test_add_members_dry_run_works(monkeypatch):
    """It aborts when run with --dry-run option"""
    runner = CliRunner();
    result = runner.invoke(cli, ['--dry-run', 'add-members', 'octodog'], input='y\n')
    assert result.exit_code == 0
    assert 'DRY RUN' in result.output


def test_add_members_aborts_on_no(monkeypatch):
    """It aborts when run with --dry-run option"""
    runner = CliRunner();
    result = runner.invoke(cli, ['--dry-run', 'add-members', 'octodog'], input='n\n')
    assert result.exit_code == 1
    assert 'Aborted!' in result.output
