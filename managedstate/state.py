from objectextensions import Extendable

from typing import Sequence, Any
from copy import deepcopy

from .keyquery import KeyQuery
from .attributename import AttributeName
from .constants import ErrorMessages


class State(Extendable):
    def __init__(self, initial_state: Any = None):
        super().__init__()

        self.__state = try_copy(initial_state) or {}

    def get(self, path_keys: Sequence[Any] = (), defaults: Sequence[Any] = ()) -> Any:
        """
        Drills into the state object using the provided path keys in sequence.
        Any time progressing further into the state object fails, the default value at the relevant index of defaults
        is substituted in.
        Returns a copy of the drilled-down state object
        """

        return try_copy(self._get_working_state(path_keys, defaults))

    def set(self, value: Any, path_keys: Sequence[Any] = (), defaults: Sequence[Any] = ()) -> None:
        """
        Drills into the state object using the provided path keys in sequence.
        Any time progressing further into the state object fails, the default value at the relevant index of defaults
        is substituted in.
        The final path key is used as the index to store a copy of the provided value at
        inside the drilled-down state object
        """

        value = try_copy(value)

        if not path_keys:
            self.__state = value
            return

        path_keys, set_key = path_keys[:-1], path_keys[-1]
        working_state = self._get_working_state(path_keys, defaults)

        if issubclass(type(set_key), KeyQuery):
            set_key = set_key(try_copy(working_state))

        if issubclass(type(set_key), AttributeName):
            setattr(working_state, set_key.name, value)

        else:  # Assume set key is a container index if not an attribute name
            working_state[set_key] = value

    def _get_working_state(self, path_keys, defaults):
        """
        Used internally to drill into the state object when a get or set operation is carried out
        """

        working_state = self.__state
        for path_index, path_key in enumerate(path_keys):
            if issubclass(type(path_key), KeyQuery):  # Resolve any KeyQuery instances first
                path_key = path_key(try_copy(working_state))

            if issubclass(type(path_key), AttributeName):
                try:
                    working_state = getattr(working_state, path_key.name)
                except AttributeError:
                    try:
                        working_state = defaults[path_index]
                    except IndexError:
                        ErrorMessages.no_default(path_index)

            else:  # Assume path key is a container index if not an attribute name
                try:
                    working_state = working_state[path_key]
                except:
                    try:
                        working_state = defaults[path_index]
                    except IndexError:
                        ErrorMessages.no_default(path_index)

        return working_state


def try_copy(item: Any) -> Any:
    """
    A failsafe deepcopy wrapper
    """

    try:
        return deepcopy(item)

    except:
        return item
