from typing import Callable, Any


class KeyQuery:
    """
    Instances of this class can be provided as path keys when getting or setting the state,
    to indicate that the next nesting level of the state should be accessed via the key returned
    from the stored function below.
    The function will receive a copy of the state object at the current level of nesting
    in order to determine what key to return
    """

    __hash__ = None
    """
    As this class is used indirectly to determine the method of access for the state object,
    it will never be used as a direct index. Thus, it should never be set as a key.
    """

    def __init__(self, get_path_key: Callable[[Any], Any]):
        self._function = get_path_key

    def __call__(self, sub_state: Any) -> Any:
        return self._function(sub_state)
