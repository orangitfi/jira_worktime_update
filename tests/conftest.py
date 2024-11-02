# tests/conftest.py
import os
import pytest


@pytest.fixture(autouse=True)
def set_env_vars():
    """Fixture to set environment variables required for tests."""
    os.environ["JIRA_URL"] = "https://dummy-jira-instance.atlassian.net"
    os.environ["JIRA_ACCOUNT"] = "dummy@example.com"
    os.environ["JIRA_API_KEY"] = "dummy-api-key"

    # Cleanup after tests
    yield
    os.environ.pop("JIRA_URL", None)
    os.environ.pop("JIRA_ACCOUNT", None)
    os.environ.pop("JIRA_API_KEY", None)
