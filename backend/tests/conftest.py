import os
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("GNANI_API_KEY", "")
os.environ.setdefault("DATABASE_URL", f"sqlite:///{tempfile.gettempdir()}/envylead_test.db")

from app.core.config import get_settings
get_settings.cache_clear()

from app.main import app
from app.core.database import init_db

# remove stale test db
p = Path(os.environ["DATABASE_URL"].replace("sqlite:///", ""))
if p.exists():
    p.unlink()
init_db()

@pytest.fixture
def client():
    return TestClient(app)
