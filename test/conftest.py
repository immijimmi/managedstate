import pytest


@pytest.fixture
def res():
    class StateResources:
        value = {"key_1": 4}
        value_2 = {"key_1": [{}, {"key_2": 5}, {}]}

    return StateResources
