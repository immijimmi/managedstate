# managedstate

###### State management inspired by Redux

## Quickstart

### Setup

```python
from managedstate import State

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

state = State(initial_state=initial_state)
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


## Functionality

### Dependencies

The State class and the extensions in this package implement Extendable and Extension respectively, from [objectextensions](https://github.com/immijimmi/objectextensions).
As such, applying extensions is done by calling the class method `State.with_extensions()` and passing in the extension classes to be applied.

Example code:
```python
from managedstate import State
from managedstate.extensions import Registrar

state = State.with_extensions(Registrar)()
```

### Extensions

**Registrar**  
&nbsp;&nbsp;&nbsp;&nbsp;Allows specific get and set operations to be registered under a shorthand label for ease of use later.  
&nbsp;

**Listeners**  
&nbsp;&nbsp;&nbsp;&nbsp;Provides an easy way to attach observer methods that will be called immediately after `set()` and/or `get()`.  
&nbsp;

### Data Classes

**AttributeName**(*self, attribute_name: str*)  
&nbsp;&nbsp;&nbsp;&nbsp;An instance of this class should be provided as a path key when getting or setting the state,  
&nbsp;&nbsp;&nbsp;&nbsp;to indicate that the next nesting level of the state should be accessed via an object attribute.  
&nbsp;

**KeyQuery**(*self, path_key_getter: Callable[[Any], Any]*)  
&nbsp;&nbsp;&nbsp;&nbsp;Instances of this class can be provided as path keys when getting or setting the state,  
&nbsp;&nbsp;&nbsp;&nbsp;to indicate that the next nesting level of the state should be accessed via the path key returned  
&nbsp;&nbsp;&nbsp;&nbsp;from its stored function.  
&nbsp;&nbsp;&nbsp;&nbsp;The function will receive a copy of the state object at the current level of nesting  
&nbsp;&nbsp;&nbsp;&nbsp;in order to determine what key to return.  
&nbsp;

### Additional Info

- KeyQuery instances provided as path keys can return any valid path key, *except* another KeyQuery or a PartialQuery.
- Similarly, PartialQuery instances can return any valid path key except for another PartialQuery (they can however return a KeyQuery)
- The data classes provided in this package are not designed to be stored inside the state object themselves, and as such their `__hash__` methods have been removed.
