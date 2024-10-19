import pytest
from fastapi import Request
from lecture_4.demo_service.api.main import create_app
from lecture_4.demo_service.api.utils import user_service


def test_create_app():
    result = create_app()
    assert result.title == "Testing Demo Service"
