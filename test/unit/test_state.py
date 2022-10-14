import pytest

from managedstate import State


class TestState:
    def test_state_is_correctly_set(self, res):
        state = State()

        assert state.get() == {}

        state = State(res.value_1)

        assert state.get() == res.value_1

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

    def test_set_handles_full_list_assignment_correctly(self, res):
        state = State(res.value_2)

        state.set(True, ["key_1", 0], [[], None])

        assert state.get() == {"key_1": [True, {"key_2": 5}, {}]}

    def test_set_handles_empty_list_assignment_correctly(self, res):
        state = State(res.value_5)

        state.set(5, ["key_1", 1], [[], 0])

        assert state.get() == {"key_1": [0, 5], "key_2": True}

        state.set(True, ["key_1", 3, "test"], [[], {}])

        assert state.get() == {"key_1": [0, 5, {}, {"test": True}], "key_2": True}

    def test_set_handles_empty_list_assignment_without_default_correctly(self):
        state = State()

        # Should not be able to set the value without a corresponding default if defaults need appending
        assert pytest.raises(ValueError, state.set, "value", ["key_1", 1], [[]])

        # Should not be able to set the value without a corresponding default even if no defaults need appending
        assert pytest.raises(ValueError, state.set, "value", ["key_1", 0], [[]])
        assert pytest.raises(ValueError, state.set, "value", ["key_1", 1], [["other_value"]])

    def test_state_remains_unchanged_after_unsuccessful_set(self):
        state = State()

        try:
            state.set("value", ["key_1", 0], [[]])
        except:
            pass

        # State value should remain unchanged after unsuccessful attempts to set a value
        assert state.get() == {}
