import pytest

from managedstate import State, KeyQuery
from managedstate.extensions import Registrar, PartialQuery


class TestPartialQuery:
    def test_partialquery_without_args_raises_error(self, res):
        state = State.with_extensions(Registrar)(res.value_2)

        query = PartialQuery(lambda args: 0)

        state.register_path("label", ["key_1", query])

        assert pytest.raises(IndexError, state.registered_get, "label")
        assert pytest.raises(IndexError, state.registered_set, "value", "label")

    def test_registered_get_with_partialquery(self, res):
        state = State.with_extensions(Registrar)(res.value_2)

        query = PartialQuery(lambda args: KeyQuery(lambda substate: args))

        state.register_path("label", ["key_1", query, "key_2"])

        assert state.registered_get("label", (1,)) == 5

    def test_registered_set_last_key_partialquery(self, res):
        state = State.with_extensions(Registrar)(res.value_2)

        query = PartialQuery(lambda args: KeyQuery(lambda substate: "key"+args))

        state.register_path("label", ["key_1", 0, query])
        state.registered_set("value", "label", ("_2",))

        assert state.get(["key_1", 0, "key_2"]) == "value"
