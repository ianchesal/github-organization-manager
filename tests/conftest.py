import pytest
from os import environ


@pytest.fixture(autouse=True)
def env_setup(monkeypatch):
    if environ.get('GOM_GITHUB_TOKEN') is None:
        monkeypatch.setenv('GOM_GITHUB_TOKEN', 'some-fake-token-123456')
    if environ.get('GOM_ORG') is None:
        monkeypatch.setenv('GOM_ORG', 'some-fake-org-123456')
