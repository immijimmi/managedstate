from typing import Callable, Any, Tuple


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

    def __init__(self, path_key_getter: Callable[[Any], Any]):
        self.__function = path_key_getter
        self.__history = []

    def __call__(self, sub_state: Any) -> Any:
        result = self.__function(sub_state)
        self.__history.append(result)

        return self.__function(sub_state)

    @property
    def history(self) -> Tuple[Any]:
        return tuple(self.__history)

    def clear(self):
        self.__history.clear()
