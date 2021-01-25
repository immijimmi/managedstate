from managedstate import State
from managedstate.extensions import Listeners


class TestListeners:
    def test_added_listener_is_correctly_called(self, res, listeners_obj):
        state = State.with_extensions(Listeners)(res.value)

        state.add_listener("get", listeners_obj.add_get_path_keys_to_list)
        state.add_listener("set", listeners_obj.add_set_value_to_list)

        assert listeners_obj.list == []

        state.get(["key_1"])

        assert listeners_obj.list == [["key_1"]]

        state.set("value", ["key_1"])

        assert listeners_obj.list == [["key_1"], "value"]

    def test_listener_added_twice_is_only_called_once(self, res, listeners_obj):
        state = State.with_extensions(Listeners)(res.value)

        state.add_listener("get", listeners_obj.add_get_path_keys_to_list)
        state.add_listener("get", listeners_obj.add_get_path_keys_to_list)

        state.get(["key_1"])

        assert listeners_obj.list == [["key_1"]]

    def test_removed_listener_is_not_called(self, res, listeners_obj):
        state = State.with_extensions(Listeners)(res.value)

        state.add_listener("get", listeners_obj.add_get_path_keys_to_list)
        state.add_listener("get", listeners_obj.add_get_path_keys_to_list)
        state.remove_listener("get", listeners_obj.add_get_path_keys_to_list)

        state.get(["key_1"])

        assert listeners_obj.list == []
