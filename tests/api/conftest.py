import pytest
import pathlib

from dotenv import load_dotenv
from obs.api.app import create_app


@pytest.fixture
def client():
    app = create_app()
    client = app.test_client()

    current_path = pathlib.Path(__file__)
    dotenv_path = "tests/api/test_api.env"
    load_dotenv(dotenv_path=dotenv_path)

    yield client
