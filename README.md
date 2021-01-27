# managedstate

###### State management inspired by Redux

## Quickstart

### Setup

```python
from managedstate import State, KeyQuery, AttributeName
from managedstate.extensions import Listeners, Registrar, PartialQuery

initial_state = {
    "first_key": [
        {
            "id": 1,
            "second_key": True
        },
        {
            "id": 2,
            "second_key": False
        }
    ]
}

state = State.with_extensions(Listeners, Registrar)(initial_state=initial_state)
```

### Getting the state

- The full state object
```python
>>> state.get()
{'first_key': [{'id': 1, 'second_key': True}, {'id': 2, 'second_key': False}]}
```

- A sub-state object
```python
>>> state.get(["first_key", 0, "second_key"], defaults=[[], {}, False])
True
```

- A sub-state object, using a query function
```python
def id_is_1_query(first_key_list):
    for index, obj in enumerate(first_key_list):
        if obj["id"] == 1:
            return index
```
```python
>>> state.get(["first_key", KeyQuery(id_is_1_query), "second_key"], defaults=[[], {}, False])
True
```

### Setting the state
- The full state object
```python
>>> state.set({'first_key': [{'id': 3, 'second_key': True}, {'id': 4, 'second_key': False}]})
>>> state.get()
{'first_key': [{'id': 3, 'second_key': True}, {'id': 4, 'second_key': False}]}
```

- A sub-state object, using a query function
```python
def get_id_keyquery(_id):  # This will dynamically create the query we need, when we need it
    def id_query(substate):
        for index, obj in enumerate(substate):
            if obj["id"] == _id:
                return index
    return KeyQuery(id_query)
```
```python
>>> state.set(False, ['first_key', get_id_keyquery(3), 'second_key'], defaults=[[], {}])
>>> state.get()
{'first_key': [{'id': 3, 'second_key': False}, {'id': 4, 'second_key': False}]}
```
