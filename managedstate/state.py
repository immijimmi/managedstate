from objectextensions import Extendable

from typing import Sequence, Any

from .keyquery import KeyQuery
from .attributename import AttributeName
from .methods import Methods, ErrorMessages


class State(Extendable):
    def __init__(self, initial_state: Any = None):
        super().__init__()

        self.__state = Methods.try_copy(initial_state) if initial_state is not None else {}

    def get(self, path_keys: Sequence[Any] = (), defaults: Sequence[Any] = ()) -> Any:
        """
        Drills into the state object using the provided path keys in sequence.
        Any time progressing further into the state object fails, the default value at the relevant index of defaults
        is substituted in.
        Returns a copy of the drilled-down state object
        """

        path_keys = list(Methods.try_copy(path_keys))
        defaults = list(Methods.try_copy(defaults))

        return Methods.try_copy(self.__get_nodes(path_keys, defaults)[-1])

    def set(self, value: Any, path_keys: Sequence[Any] = (), defaults: Sequence[Any] = ()) -> None:
        """
        Drills into the state object using the provided path keys in sequence.
        Any time progressing further into the state object fails, the default value at the relevant index of defaults
        is substituted in.
        The final path key is used as the index to store a copy of the provided value at
        inside the drilled-down state object
        """

        value = Methods.try_copy(value)
        path_keys = list(Methods.try_copy(path_keys))
        defaults = list(Methods.try_copy(defaults))

        nodes = self.__get_nodes(path_keys[:-1], defaults)

        while path_keys:
            working_state = nodes.pop()  # Take the deepest remaining node within the state
            set_key = path_keys.pop()  # Take the deepest remaining path key

            if issubclass(type(set_key), KeyQuery):  # Resolve any KeyQuery instances first
                key_query = set_key
                if key_query.history:  # KeyQuery was already resolved in .__get_nodes()
                    set_key = key_query.history[-1]  # Take the last resolved value (to minimise resource usage)
                    key_query.history.clear()
                else:
                    set_key = key_query(Methods.try_copy(working_state))

            if issubclass(type(set_key), AttributeName):  # Work with any AttributeName instances
                setattr(working_state, set_key.name, value)
            else:  # Assume set_key is a container index if not an attribute name
                try:
                    working_state[set_key] = value
                # May occur if working_state is a list (or similar) without a stored value at the target index
                except IndexError as ex:
                    """
                    In a `set` operation (as opposed to a `get` operation), simply substituting in the relevant default
                    for working_state when it cannot be modified will not work;
                    this would erase any modifications that were made further into the working_state object
                    before reaching the current iteration.

                    However, if working_state is a list (or similar), it is possible to populate the list with instances
                    of the relevant default for `value` up to the desired index and then add `value` in at the index
                    indicated by the path key
                    """

                    try:  # Get the relevant default for `value`
                        nested_default = defaults[len(path_keys)]
                    except IndexError:
                        ErrorMessages.no_default(set_key)

                    try:
                        missing_indexes = set_key-len(working_state)
                        for i in range(missing_indexes):
                            # Populate list with default values up to set_key
                            working_state.append(Methods.try_copy(nested_default))

                        working_state.append(value)  # Add in current value in at the index of set_key
                    except:  # Unable to work with path key at all
                        raise ex  # Raise previous IndexError, as working_state did not turn out to be usable as a list

            value = working_state  # This working_state will now be stored into the next node up

        self.__state = value

    def __get_nodes(self, path_keys, defaults):
        """
        Used internally to drill into the state object when a get or set operation is carried out
        """

        working_state = self.__state
        nodes = [working_state]

        for path_index, path_key in enumerate(path_keys):
            if issubclass(type(path_key), KeyQuery):  # Resolve any KeyQuery instances first
                path_key = path_key(Methods.try_copy(working_state))

            if issubclass(type(path_key), AttributeName):  # Work with any AttributeName instances
                try:
                    working_state = getattr(working_state, path_key.name)
                except AttributeError:  # No attribute found, use default value
                    try:
                        working_state = defaults[path_index]
                    except IndexError:
                        ErrorMessages.no_default(path_index)
            else:  # Assume path key is a container index if not an attribute name
                try:
                    working_state = working_state[path_key]
                except:  # Unable to work with path key at all, use default value
                    try:
                        working_state = defaults[path_index]
                    except IndexError:
                        ErrorMessages.no_default(path_index)

            nodes.append(working_state)

        return nodes
