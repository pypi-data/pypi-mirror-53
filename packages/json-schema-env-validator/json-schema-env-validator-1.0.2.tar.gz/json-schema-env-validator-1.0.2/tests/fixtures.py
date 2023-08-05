import pytest
import os


@pytest.fixture()
def env():
    os.environ.clear()
