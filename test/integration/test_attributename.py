from managedstate import State, AttributeName


class TestAttributeName:
    def test_get_uses_attributename_correctly(self, res):
        state = State(res.value_4)

        assert state.get(["key_2", AttributeName("attribute_1"), "key_3"]) == 7

    def test_set_applies_attributename_correctly(self, res):
        state = State(res.value_4)

        state.set("value", ["key_2", AttributeName("attribute_2")])

        assert state.get(["key_2", AttributeName("attribute_2")]) == "value"
