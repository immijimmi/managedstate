from managedstate import State
from managedstate.extensions import Registrar


class TestRegistrar:
    def test_registered_set_uses_correct_path_keys(self, res):
        state = State.with_extensions(Registrar)(res.value_2)

        state.register("test_label", ["key_1", 1, "key_2"])

        state.registered_set("value", "test_label")

        assert state.get() == {"key_1": [{}, {"key_2": "value"}, {}]}

    def test_registered_get_uses_correct_path_keys(self, res):
        state = State.with_extensions(Registrar)(res.value_2)

        state.register("test_label", ["key_1", 1, "key_2"])

        assert state.registered_get("test_label") == 5

    def test_registered_get_uses_correct_defaults(self, res):
        state = State.with_extensions(Registrar)(res.value_2)

        state.register("test_label", ["key_1", "wrong_key_type", "key_2"], [[], {}, 0])

        assert state.registered_get("test_label") == 0

    def test_registered_set_uses_correct_defaults(self, res):
        state = State.with_extensions(Registrar)(res.value_3)

        state.register("test_label", ["key_1", "nonexistent_key", "key_4"], [{}, {}, 0])

        state.registered_set("value", "test_label")

        assert state.get() == {"key_1": {"key_2": [], "key_3": {"key_4": 8}, "nonexistent_key": {"key_4": "value"}}}
