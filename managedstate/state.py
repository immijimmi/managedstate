from objectextensions import Extendable

from typing import Sequence, Any

from .recursivenode import RecursiveNode


class State(Extendable):
    def __init__(self, initial_state: Any = None):
        self.__state = initial_state or {}

    def get(self, path_keys: Sequence[Any] = (), defaults: Sequence[Any] = ()) -> Any:
        """
        Drills into the state object using the provided path keys in sequence.
        Any time progressing further into the state object fails, the default value at the relevant index of defaults
        is substituted in.
        Once all path keys have been applied, the drilled-down state object is returned
        """

        return RecursiveNode(self.__state, path_keys, defaults).get()

    def set(self, value: Any, path_keys: Sequence[Any] = (), defaults: Sequence[Any] = ()) -> None:
        """
        Drills into the state object using the provided path keys in sequence.
        Any time progressing further into the state object fails, the default value at the relevant index of defaults
        is substituted in.
        Once all path keys have been applied, the current subset of the state object is set equal to the provided value
        """

        working_state = RecursiveNode(self.__state, path_keys, defaults)
        working_state.set(value)
        self.__state = working_state.value
