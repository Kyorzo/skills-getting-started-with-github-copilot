import sys
import copy
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Ensure src is importable
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
import app as app_module

# Keep an original deep copy of activities to reset between tests
ORIGINAL_ACTIVITIES = copy.deepcopy(app_module.activities)


@pytest.fixture
def app():
    return app_module.app


@pytest.fixture
def client(app):
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    # Reset the in-memory database before each test
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))
    yield
    # Ensure it's reset after test as well
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))
