import pytest

from managedstate import State


@pytest.fixture
def res():
    class StateResources:
        value = {"key_1": 4}
        value_2 = {"key_1": [{}, {"key_2": 5}, {}]}

    return StateResources


class TestState:
    def test_state_is_correctly_set(self, res):
        state = State()

        assert state.get() == {}

        state = State(res.value)

        assert state.get() == res.value

        state = State()
        state.set(res.value_2)

        assert state.get() == res.value_2

    def test_get_with_path_keys(self, res):
        state = State(res.value_2)

        assert state.get(["key_1", 1, "key_2"]) == 5

    def test_set_with_path_keys(self, res):
        state = State(res.value_2)

        state.set([13, 37], ["key_1", 0, "key_2"])  # Setting to a key that does not yet exist should add the new value

        assert state.get(["key_1", 0, "key_2"]) == [13, 37]

        state.set("value", ["key_1", 0, "key_2"])  # Setting to a key that exists should replace the existing value

        assert state.get(["key_1", 0, "key_2"]) == "value"

    def test_invalid_get_no_defaults_raises_error(self, res):
        state = State(res.value_2)

        assert pytest.raises(ValueError, state.get, ["key_1", "wrong_key_type"])
        assert pytest.raises(ValueError, state.get, ["nonexistent_key", 1, "key_2"])

    def test_invalid_set_no_defaults_raises_error(self, res):
        state = State(res.value_2)

        assert pytest.raises(ValueError, state.set, "value", ["key_1", "wrong_key_type", "key_2"])
        assert pytest.raises(ValueError, state.set, "value", ["nonexistent_key", 1, "key_2"])

    def test_get_with_defaults(self, res):
        state = State(res.value_2)

        assert state.get(["key_1", 0, "key_2"], [[], {}, 0]) == 0

    def test_set_with_defaults(self, res):
        state = State(res.value_2)

        state.set(6, ["key_1", 0, "key_2"], [[], {}, 0])

        assert state.get(["key_1", 0, "key_2"]) == 6

    def test_fewer_defaults_than_necessary_raises_error(self, res):
        state = State(res.value_2)

        # Not enough defaults provided
        assert pytest.raises(ValueError, state.get, ["key_1", 0, "nonexistent_key"], [[], {}])
        assert pytest.raises(ValueError, state.set, "value", ["key_1", "wrong_key_type", "key_2"], [[]])

        # Enough defaults provided
        state.set("value", ["key_1", 1, "key_2"], [[], {}])  # Set operation only needs one less path key

        assert state.get(["key_1", "wrong_key_type", "key_2"], [[], {}, 0]) == 0

    def test_invalid_necessary_defaults_raises_error(self, res):
        state = State(res.value_2)

        # Invalid defaults provided and used
        assert pytest.raises(TypeError, state.set, "value", ["key_1", "wrong_key_type", "key_2"], [[], []])

        # Invalid defaults provided but not used
        state.set("value", ["key_1", 0, "key_2"], [[], []])

        assert state.get(["key_1", 0, "key_2"], [[], [], 0]) == "value"
