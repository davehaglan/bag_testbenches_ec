# -*- coding: utf-8 -*-

import pytest

from bag.env import create_tech_info
from bag.layout.tech import TechInfo
from bag.design.database import ModuleDB


@pytest.fixture(scope='session')
def tech_info() -> TechInfo:
    return create_tech_info()


@pytest.fixture
def module_db(tech_info: TechInfo) -> ModuleDB:
    return ModuleDB(tech_info, 'PYTEST')
