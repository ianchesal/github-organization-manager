import pytest
from os import environ


@pytest.fixture(autouse=True)
def env_setup(monkeypatch):
    if environ.get('GOM_GITHUB_TOKEN') is None:
        monkeypatch.setenv('GOM_GITHUB_TOKEN', 'some-fake-token-123456')
    if environ.get('GOM_ORG') is None:
        monkeypatch.setenv('GOM_ORG', 'some-fake-org-123456')

@pytest.fixture(scope='module')
def vcr_config():
    return {
        # Replace the Authorization request header with "DUMMY" in cassettes
        "filter_headers": [('Authorization', 'DUMMY')],
    }
