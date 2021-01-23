from typing import Callable, Any


class KeyQuery:
    """
    An instance of this class should be provided as a path key when getting or setting the state,
    to indicate that the next nesting level of the state should be accessed via the index returned
    from the stored query function.
    The query function will receive a copy of the state object at the current level of nesting
    in order to determine what index to return
    """

    __hash__ = None
    """
    As this class is used indirectly to determine the method of access for the state object,
    it will never be used as a direct index. Thus, it should never be set as a key.
    """

    def __init__(self, query_function: Callable[[Any], Any]):
        self.__query = query_function

    def __call__(self, sub_state: Any) -> Any:
        return self.__query(sub_state)
