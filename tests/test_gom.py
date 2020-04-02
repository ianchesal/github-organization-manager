import pytest
from click.testing import CliRunner
from gom import cli


def test_cli_requires_an_org(monkeypatch):
    """It errors if you don't provide --org"""
    monkeypatch.delenv('GOM_ORG', raising=False)
    runner = CliRunner();
    result = runner.invoke(cli, ['list-organizations'])
    assert 'Error: missing required environment variable: GOM_ORG' in result.output
    assert result.exit_code == 1


def test_cli_requires_a_token(monkeypatch):
    """It errors if you don't provide a GOM_GITHUB_TOKEN env var"""
    monkeypatch.delenv('GOM_GITHUB_TOKEN', raising=False)
    runner = CliRunner();
    result = runner.invoke(cli, ['list-organizations'])
    assert 'Error: missing required environment variable: GOM_GITHUB_TOKEN' in result.output
    assert result.exit_code == 1


@pytest.mark.vcr()
def test_cli_reads_org_from_environment(monkeypatch):
    """It can get the organization name from an env var"""
    runner = CliRunner();
    result = runner.invoke(cli, ['list-organizations'])
    assert result.exit_code == 0


@pytest.mark.vcr()
def test_list_organizations(monkeypatch):
    """It can retrieve all the organizations for a user"""
    runner = CliRunner();
    result = runner.invoke(cli, ['list-organizations'])
    assert 'tinwhiskersband' in result.output
    assert result.exit_code == 0


@pytest.mark.vcr()
def test_list_members(monkeypatch):
    """It can retrieve all the members for an organizations"""
    runner = CliRunner();
    result = runner.invoke(cli, ['list-members'])
    assert 'ianchesal' in result.output
    assert result.exit_code == 0


def test_add_members_dry_run_works(monkeypatch):
    """It aborts when run with --dry-run option"""
    runner = CliRunner();
    result = runner.invoke(cli, ['--dry-run', 'add-members', 'octodog'], input='y\n')
    assert 'DRY RUN' in result.output
    assert result.exit_code == 0


def test_add_members_aborts_on_no(monkeypatch):
    """It aborts when run with --dry-run option"""
    runner = CliRunner();
    result = runner.invoke(cli, ['--dry-run', 'add-members', 'octodog'], input='n\n')
    assert 'Aborted!' in result.output
    assert result.exit_code == 1
