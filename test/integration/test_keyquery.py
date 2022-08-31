from managedstate import State, KeyQuery


class TestKeyQuery:
    def test_get_uses_key_query_correctly(self, res):
        state = State(res.value_2)

        query = KeyQuery(lambda substate: substate.index({"key_2": 5}))

        assert state.get(["key_1", query, "key_2"]) == 5

    def test_set_uses_key_query_correctly(self, res):
        state = State(res.value_2)

        query = KeyQuery(lambda substate: substate.index({"key_2": 5}))

        state.set("value", ["key_1", query, "key_2"])

        assert state.get(["key_1", 1, "key_2"]) == "value"
