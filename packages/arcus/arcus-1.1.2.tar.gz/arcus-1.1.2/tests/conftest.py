import os

import pytest
import requests_mock

from arcus import Client


@pytest.fixture
def client():
    yield Client(sandbox=True)


@pytest.fixture
def client_proxy():
    proxy = os.environ['ARCUS_PROXY']
    with requests_mock.mock() as m:
        m.get(f'{proxy}/account', json=dict(
            name='Cuenca',
            balance=60454.43,
            minimum_balance=0.0,
            currency='MXN'
        )
        )
        m.post(
            f'{proxy}/account',
            json=dict(
                message='Missing Authentication Token'
            ),
            status_code=403
        )
        yield Client(sandbox=True, proxy=proxy)
