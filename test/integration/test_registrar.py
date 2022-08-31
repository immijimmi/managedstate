import pytest

from managedstate import State
from managedstate import AttributeName
from managedstate.extensions import Registrar
from managedstate.extensions.registrar import Keys


class TestRegistrar:
    def test_registered_set_uses_correct_path_keys(self, res):
        state = State.with_extensions(Registrar)(res.value_2)

        state.register_path("test_label", ["key_1", 1, "key_2"])
        state.registered_set("value", "test_label")

        assert state.get() == {"key_1": [{}, {"key_2": "value"}, {}]}

    def test_registered_get_uses_correct_path_keys(self, res):
        state = State.with_extensions(Registrar)(res.value_2)

        state.register_path("test_label", ["key_1", 1, "key_2"])

        assert state.registered_get("test_label") == 5

    def test_registered_get_uses_correct_defaults(self, res):
        state = State.with_extensions(Registrar)(res.value_2)

        state.register_path("test_label", ["key_1", "wrong_key_type", "key_2"], [[], {}, 0])

        assert state.registered_get("test_label") == 0

    def test_registered_set_uses_correct_defaults(self, res):
        state = State.with_extensions(Registrar)(res.value_3)

        state.register_path("test_label", ["key_1", "nonexistent_key", "key_4"], [{}, {}, 0])
        state.registered_set("value", "test_label")

        assert state.get() == {"key_1": {"key_2": [], "key_3": {"key_4": 8}, "nonexistent_key": {"key_4": "value"}}}

    def test_registered_set_no_pathkeys(self, res):
        state = State.with_extensions(Registrar)(res.value_1)

        state.register_path("test_label", [])
        state.registered_set(8, "test_label")

        assert state.get() == 8

    def test_registered_paths_returns_correct_values(self):
        state = State.with_extensions(Registrar)()

        state.register_path("test_label", ["key", 2], [(0,), None])
        state.register_path("test_label_2", [])

        registered_paths = state.registered_paths

        assert len(registered_paths) == 2

        # test_label checks
        test_label_values = registered_paths["test_label"]

        assert len(test_label_values) == 2

        test_label_path_keys = test_label_values[Keys.PATH_KEYS]

        assert len(test_label_path_keys) == 2
        assert test_label_path_keys[0] == "key"
        assert test_label_path_keys[1] == 2

        test_label_defaults = test_label_values[Keys.DEFAULTS]

        assert len(test_label_defaults) == 2
        assert test_label_defaults[0] == (0,)
        assert test_label_defaults[1] is None

        # test_label_2 checks
        test_label_2_values = registered_paths["test_label_2"]

        assert len(test_label_2_values) == 2

        test_label_2_path_keys = test_label_2_values[Keys.PATH_KEYS]

        assert len(test_label_2_path_keys) == 0

        test_label_2_defaults = test_label_2_values[Keys.DEFAULTS]

        assert len(test_label_2_defaults) == 0

    def test_registered_paths_are_correctly_overwritten(self):
        state = State.with_extensions(Registrar)()

        state.register_path("test_label", ["key", 2], [(0,), None])
        state.register_path("test_label", [])

        registered_paths = state.registered_paths
        test_label_values = registered_paths["test_label"]

        assert len(test_label_values) == 2

        test_label_path_keys = test_label_values[Keys.PATH_KEYS]

        assert len(test_label_path_keys) == 0

        test_label_defaults = test_label_values[Keys.DEFAULTS]

        assert len(test_label_defaults) == 0

    def test_editing_registered_paths_does_not_affect_stored_dict(self):
        state = State.with_extensions(Registrar)()

        state.register_path("test_label", [])

        registered_paths = state.registered_paths
        registered_paths.clear()

        registered_paths_2 = state.registered_paths

        assert len(registered_paths) == 0
        assert len(registered_paths_2) == 1

    def test_get_shape_returns_correct_state_shape(self):
        state = State.with_extensions(Registrar)()

        state.register_path("test_label", [])

        state.register_path("test_label_2", [0], [{}])
        state.register_path("test_label_3", [0, "key", 0], [{}, [{}], 3])

        state_shape = state.get_shape()
        assert state_shape == {0: {"key": [3]}}

    def test_get_shape_raises_error_with_conflicting_registered_paths(self):
        state = State.with_extensions(Registrar)()

        state.register_path("test_label", [0, "key", 0], [{}, [{}], 3])
        state.register_path("test_label_2", [0, "key", 0], [{}, [False], 3])

        assert pytest.raises(RuntimeError, state.get_shape)

    def test_get_shape_correctly_handles_attributename_objects(self):
        class ThrowawayClass:
            def __eq__(self, other):
                return issubclass(type(other), ThrowawayClass) and (self.value == other.value)

            def __init__(self, value):
                self.value = value

        state = State.with_extensions(Registrar)()

        state.register_path("test_label", ["throwaway", AttributeName("value")], [ThrowawayClass({}), {}])

        assert state.get_shape() == {"throwaway": ThrowawayClass({})}
