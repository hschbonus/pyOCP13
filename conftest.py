"""Shared pytest configuration."""
import pytest
import sentry_sdk


@pytest.fixture(autouse=True, scope="session")
def disable_sentry():
    """Prevent the tests from sending events to the real Sentry project."""
    sentry_sdk.init(dsn="")
