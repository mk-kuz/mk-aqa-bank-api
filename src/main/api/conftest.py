import logging
from collections.abc import Generator
from typing import Any, List

import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.api_fixture import api_manager
from src.main.api.fixtures.db_fixture import *
from src.main.api.fixtures.preconditions import *
from src.main.api.fixtures.object_fixture import create_credit_user_request, create_user_request
from src.main.api.models.create_user_response import CreateUserResponse


@pytest.fixture
def created_obj() -> Generator[List[Any], None, None]:
    objects: List[Any] = []
    yield objects
    clean_user(objects)


def clean_user(objects: List[Any]):
    api_manager = ApiManager(objects)
    for u in objects:
        if isinstance(u, CreateUserResponse):
            api_manager.admin_steps.delete_user(u.id)
        else:
            logging.warning(f"Error in delete user_id: {u.id}")
