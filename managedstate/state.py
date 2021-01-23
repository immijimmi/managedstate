from objectextensions import Extendable

from typing import Sequence, Any

from .recursiveNode import RecursiveNode


class State(Extendable):
    def __init__(self, initial_state: Any = None):
        self.__state = initial_state or {}

    def get(self, path_keys: Sequence[Any] = (), defaults: Sequence[Any] = ()) -> Any:
        return RecursiveNode(self.__state, path_keys, defaults).get()

    def set(self, value: Any, path_keys: Sequence[Any] = (), defaults: Sequence[Any] = ()) -> None:
        working_state = RecursiveNode(self.__state, path_keys, defaults)
        working_state.set(value)
        self.__state = working_state.value
