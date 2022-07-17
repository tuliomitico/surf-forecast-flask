import pytest
from flask import Flask

from src.server import create_app

@pytest.fixture(scope='session')
def app():
  app = create_app('src.config.TestingConfig')
  yield app

@pytest.fixture(scope='session')
def client(app: Flask):
  return app.test_client()

