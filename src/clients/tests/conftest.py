from flask import Flask
import pytest

from src.server import create_app

@pytest.fixture
def test_request(app: Flask):
  ctx = app.test_request_context()
  ctx.push()
  yield ctx
  ctx.pop()

@pytest.fixture
def app():
  app = create_app('src.config.TestingConfig')
  yield app