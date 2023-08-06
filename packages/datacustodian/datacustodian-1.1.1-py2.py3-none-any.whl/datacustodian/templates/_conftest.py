import pytest

@pytest.fixture
def client():
    from {{ name }} import app
    from datacustodian.base import set_testmode
    set_testmode(True)

    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
